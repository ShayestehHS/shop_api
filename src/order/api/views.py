import json

import requests
from django.conf import settings
from rest_framework import status
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.models import Cart
from cart.permissions import IsCartHaveProduct
from order.models import Order
from order.api.serializers import OrderCreateSerializer, OrderListSerializer
from order.permissions import IsNotHavePaidOrder, IsOrderNotPaid
from order.utils import update_products_count
from product.models import Product
from shop_api.utils import create_response_base_on_post_res, send_request_to_zp


class OrderPagination(PageNumberPagination):
    page_size = settings.ORDER_PAGINATION
    page_size_query_param = 'page_size'
    max_page_size = settings.ORDER_MAX_PAGINATION


class OrderListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderListSerializer
    pagination_class = OrderPagination

    def get_queryset(self):
        if self.queryset:
            return self.queryset
        order = Order.objects.filter(user=self.request.user).only('user', 'payable_amount', 'is_paid', 'coupon')
        self.queryset = order
        return order

    def list(self, request, *args, **kwargs):
        if not self.get_queryset().exists():
            return Response({"Not found": "You don't have any order yet."})
        return super(OrderListAPIView, self).list(request, *args, **kwargs)


class OrderCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsNotHavePaidOrder, IsCartHaveProduct]
    serializer_class = OrderCreateSerializer
    cart = None

    def get_object(self):
        if self.cart is not None:
            return self.cart
        obj = get_object_or_404(Cart, user=self.request.user)
        self.check_object_permissions(self.request, obj)
        self.cart = obj
        return obj

    def post(self, request, *args, **kwargs):
        cart: Cart = self.get_object()

        kwargs['cart'] = cart
        kwargs['products'] = Product.objects.filter(cart=cart, in_store=True)
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        context = self.get_serializer_context()
        context.update({'cart': kwargs.get('cart'), 'products': kwargs.get('products')})
        serializer = self.serializer_class(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)

        serializer.create(serializer.validated_data)
        return Response({'Result': 'Order is created.'}, status=status.HTTP_201_CREATED)


class OrderDeleteAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsOrderNotPaid]
    queryset = Order.objects.all()
    lookup_field = 'id'


class VerifyAPIView(APIView):
    def get(self, request, format=None):
        if request.GET.get('Status') != 'OK':
            return Response({"Error": 'Transaction failed or canceled by user'}, status=status.HTTP_400_BAD_REQUEST)

        authority = request.GET['Authority']
        order = get_object_or_404(Order, authority=authority)

        req_header = {"accept": "application/json", "content-type": "application/json"}
        req_data = {
            "merchant_id": settings.MERCHANT,
            "amount": int(order.payable_amount) * 1000,
            "authority": authority,
        }

        res_post = requests.post(url=settings.ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
        response: Response = create_response_base_on_post_res(res_post)
        if response.status_code == 200 or (not order.is_paid and response.status_code == 204):
            order.is_paid = True
            order.save(update_fields=['is_paid'])
            cart = Cart.objects.get(order_authority=authority)
            cart.products.clear()
            update_products_count(order)
        return response


class PaymentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        order = Order.objects.filter(user=user, is_paid=False).only('payable_amount')
        if not order.exists():
            return Response({"Error": "You don't have any unpaid order."}, status.HTTP_404_NOT_FOUND)
        elif order.count() != 1:
            return Response({"Error": "You can't have more than one unpaid order at the same time."}, status=status.HTTP_400_BAD_REQUEST)

        order = order.first()
        cart = get_object_or_404(Cart, user=user)
        return send_request_to_zp(request, order, cart, int(order.payable_amount) * 1000, user.email)

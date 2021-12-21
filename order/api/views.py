import json

import requests
from django.conf import settings
from django.http import JsonResponse
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.models import Cart
from order.models import Order
from order.api.serializers import OrderCreateSerializer, OrderListSerializer
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
    permission_classes = [IsAuthenticated]
    serializer_class = OrderCreateSerializer

    def post(self, request, *args, **kwargs):
        if Order.objects.filter(user=self.request.user, is_paid=False).exists():
            return Response({"Error": "You can't have more than one unpaid order at the same time."}, status=status.HTTP_400_BAD_REQUEST)

        cart = Cart.objects.filter(user=self.request.user).only('products', 'sum_prices')
        if not cart.exists():
            return Response({"Error": "You don't have any cart."}, status=status.HTTP_404_NOT_FOUND)
        elif cart.first().sum_prices == 0:
            return Response({"Error": "You don't have any product in your cart."}, status=status.HTTP_400_BAD_REQUEST)

        kwargs['cart'] = cart.first()
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        cart = kwargs.get('cart')
        context = self.get_serializer_context()
        context.update({'cart': cart})

        serializer = self.serializer_class(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.create(serializer.validated_data)
        return Response({'Result': 'Order is created.'}, status=status.HTTP_201_CREATED)


class VerifyAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        if request.GET.get('Status') != 'OK':
            return Response({"Error": 'Transaction failed or canceled by user'}, status=status.HTTP_400_BAD_REQUEST)
        order = Order.objects \
            .filter(user=request.user, is_paid=False) \
            .only('payable_amount') \
            .first()
        req_header = {"accept": "application/json", "content-type": "application/json"}
        req_data = {
            "merchant_id": settings.MERCHANT,
            "amount": order.payable_amount,
            "authority": request.GET['Authority'],
        }

        res_post = requests.post(url=settings.ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
        response: Response = create_response_base_on_post_res(res_post)
        if response.status_code == 200:
            order.is_paid = True
            order.save(update_fields=['is_paid'])

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
        return send_request_to_zp(request, int(order.payable_amount) * 1000, user.email)

from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from cart.models import Cart
from order.models import Order
from order.api.serializers import OrderCreateSerializer, OrderListSerializer


class OrderListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderListSerializer

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

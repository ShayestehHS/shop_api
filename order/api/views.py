from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from order.models import Order
from order.api.serializers import OrderListSerializer


class OrderListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderListSerializer

    def get_queryset(self):
        if self.queryset:
            return self.queryset
        order = Order.objects.filter(user=self.request.user).only(*self.serializer_class.Meta.fields)
        self.queryset = order
        return order

    def list(self, request, *args, **kwargs):
        if not self.get_queryset().exists():
            return Response({"Not found": "You don't have any order yet."})
        return super(OrderListAPIView, self).list(request, *args, **kwargs)

#
# class OrderCreateAPIView(CreateAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = OrderCreateSerializer

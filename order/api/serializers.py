from rest_framework import serializers

from order.models import Coupon, Order


class OrderListSerializer(serializers.ModelSerializer):
    is_used_coupon = serializers.SerializerMethodField()

    def get_is_used_coupon(self, obj: Order):
        return bool(obj.coupon_id)

    class Meta:
        model = Order
        fields = ['user', 'coupon', 'payable_amount', 'is_paid']

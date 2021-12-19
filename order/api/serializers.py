from rest_framework import serializers

from order.models import Coupon, Order


class OrderListSerializer(serializers.ModelSerializer):
    coupon = serializers.SerializerMethodField()

    def get_coupon(self, obj: Order):
        if obj.coupon:
            coupon = Coupon.objects.filter(order=obj).only('is_valid').first()
            return coupon.is_valid
        return False

    class Meta:
        model = Order
        fields = ['user', 'coupon', 'payable_amount', 'is_paid']

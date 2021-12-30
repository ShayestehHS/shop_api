from rest_framework import serializers

from cart.models import Cart
from order.models import Coupon, Order, Price
from product.utils import get_products_price, get_sum_price


def create_price(order: Order, products, products_price):
    bulk_list = []
    for inx, product in enumerate(products):
        product_price = products_price[inx]
        bulk_list.append(Price(order=order, product=product, amount=product_price))
    Price.objects.bulk_create(bulk_list)


class OrderListSerializer(serializers.ModelSerializer):
    is_used_coupon = serializers.SerializerMethodField()
    products = serializers.SerializerMethodField()

    def get_products(self, obj: Order):
        prices = Price.objects.filter(order=obj).prefetch_related('product')
        result = {}
        for price in prices:
            result.update({price.product.name: price.amount})
        return result

    def get_is_used_coupon(self, obj: Order):
        return bool(obj.coupon_id)

    class Meta:
        model = Order
        fields = ['id', 'user', 'products', 'is_used_coupon', 'payable_amount', 'is_paid']


class OrderCreateSerializer(serializers.ModelSerializer):
    coupon_code = serializers.CharField(max_length=15, allow_blank=True, help_text="Maximum length for code is 15 character.")

    class Meta:
        model = Order
        fields = ['address', 'coupon_code']

    def validate_coupon_code(self, value):
        if value is '':
            return value

        coupon = Coupon.objects.filter(code=value).only('discount_amount', 'discount_percent')
        if not coupon.exists():
            raise serializers.ValidationError({'Coupon': "Coupon code is not valid"})
        self.context['coupon'] = coupon.first()
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        cart: Cart = self.context['cart']  # Set in view
        coupon = self.context.get('coupon')  # Set in validate_coupon_code
        validated_data.pop('coupon_code')

        products_price = get_products_price(products)
        payable_amount = get_sum_price(products_price)
        if coupon and coupon.discount_percent != 0:
            new_amount = payable_amount * (100 - coupon.discount_percent)
        elif coupon and coupon.discount_amount != 0:
            new_amount = payable_amount - coupon.discount_amount

        discount = payable_amount - new_amount
        order = Order.objects.create(**validated_data,
                                     user=user, discount=discount,
                                     payable_amount=payable_amount)
        order.products.add(cart.products.values_list('id', flat=True).first())
        create_price(order, products, products_price)
        cart.products.clear()
        return order

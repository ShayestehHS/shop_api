from rest_framework import serializers

from cart.models import Cart


class CartProductSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    def get_products(self, obj: Cart):
        return obj.products.values('name')

    class Meta:
        model = Cart
        fields = ['products']

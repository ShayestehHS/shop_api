from rest_framework import serializers

from cart.models import Cart


class CartSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    def get_products(self, obj: Cart):
        return obj.products.values('id', 'name')

    class Meta:
        model = Cart
        exclude = ('user',)


class CartListProductsSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    def get_products(self, obj: Cart):
        return obj.products.values('id', 'name')

    class Meta:
        model = Cart
        fields = ['products']

from rest_framework import serializers

from product.models import Product


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ['slug', 'in_store', 'timestamp', 'last_update', 'average_rate']
        extra_kwargs = {'color': {'initial': 'yellow'}}


class ProductRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ['slug', 'last_update', 'purchase_price']


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ['slug', 'last_update', 'body', 'count', 'stone_price', 'purchase_price']

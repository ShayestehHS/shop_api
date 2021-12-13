from rest_framework import serializers

from product.models import Product


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ['slug', 'in_store', 'timestamp', 'last_update', 'average_rating']
        extra_kwargs = {'color': {'initial': 'yellow'}}


class ProductRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ['slug', 'last_update', 'purchase_price']

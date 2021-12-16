from django.core.cache import cache
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAdminUser

from product.api.serializers import ProductCreateSerializer, ProductRetrieveSerializer, ProductListSerializer
from product.models import Product


class ProductCreate(CreateAPIView):
    serializer_class = ProductCreateSerializer
    permission_classes = [IsAdminUser]


class ProductRetrieve(RetrieveAPIView):
    serializer_class = ProductRetrieveSerializer

    def get_object(self):
        obj = Product.objects \
            .filter(pk=self.kwargs.get('pk')) \
            .defer(*self.serializer_class.Meta.exclude)

        if not obj.exists():
            raise NotFound(detail="Error 404, product not found", code=status.HTTP_400_BAD_REQUEST)
        return obj.first()


class ProductList(ListAPIView):
    serializer_class = ProductListSerializer
    filterset_fields = ['in_store', 'material']
    search_filter = ['name', 'slug', 'body', 'tags__name', 'tags__slug']
    ordering_fields = ['timestamp', 'average_rate']

    def get_queryset(self):
        if 'products' in cache:
            products = cache.get('products')
            if products.exists(): return products

        qs = Product.objects \
            .filter(in_store=True) \
            .defer(*self.serializer_class.Meta.exclude)
        if not qs.exists(): raise NotFound(detail="Error 404, Our store is empty", code=404)

        cache.set('products', qs)
        return qs

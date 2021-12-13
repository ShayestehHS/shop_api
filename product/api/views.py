from rest_framework.exceptions import NotFound
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAdminUser

from product.api.serializers import ProductCreateSerializer, ProductRetrieveSerializer
from product.models import Product


class ProductCreate(CreateAPIView):
    serializer_class = ProductCreateSerializer
    permission_classes = [IsAdminUser]


class ProductRetrieve(RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductRetrieveSerializer

    def get_object(self):
        obj = Product.objects \
            .filter(pk=self.kwargs.get('pk')) \
            .defer(*self.serializer_class.Meta.exclude)

        if not obj.exists():
            raise NotFound(detail="Error 404, product not found", code=404)
        return obj.first()

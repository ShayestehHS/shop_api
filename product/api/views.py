from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAdminUser

from product.api.serializers import ProductCreateSerializer


class ProductCreate(CreateAPIView):
    serializer_class = ProductCreateSerializer
    permission_classes = [IsAdminUser]

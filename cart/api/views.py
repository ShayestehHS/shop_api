from rest_framework import status
from rest_framework.generics import ListAPIView, UpdateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from cart.api.serializers import CartProductSerializer
from cart.models import Cart
from product.models import Product


class CartAddProduct(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartProductSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = Cart.objects.get(user_id=self.request.user.id)
        serializer = self.serializer_class(instance=instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        products = serializer.validated_data['products']
        instance.products.add(*products)

        return Response(data={'r': 'success'}, status=status.HTTP_200_OK)


class CartAddProductURL(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartProductSerializer

    def get(self, request, *args, **kwargs):
        cart = Cart.objects.get(user=self.request.user)
        pk = kwargs.get('pk')
        in_cart = cart.products.filter(pk=pk).exists()
        return Response({'in_cart': in_cart}, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        cart = Cart.objects.get(user=request.user)
        product = get_object_or_404(Product, pk=pk)

        cart.products.add(product)
        serializer = self.serializer_class(cart, data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data)


class CartListProduct(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartProductSerializer

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user).only('products')

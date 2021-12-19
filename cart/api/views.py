from django.views.generic import UpdateView
from rest_framework.generics import ListAPIView, GenericAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.api.serializers import CartListProductsSerializer, CartSerializer
from cart.models import Cart
from product.models import Product


class RetrieveCart(GenericAPIView):
    http_method_names = ['get']
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    def get_object(self):
        obj = Cart.objects \
            .filter(user=self.request.user) \
            .only('products') \
            .first()
        return obj

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(instance=self.get_object(), data=request.data,context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data)


class CartListProducts(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartListProductsSerializer

    def get_queryset(self):
        qs = Cart.objects \
                 .filter(user=self.request.user) \
                 .only('products')[:1]
        return qs


class CartAddProduct(APIView):
    http_method_names = ['post']
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        product = get_object_or_404(Product, pk=pk)
        cart = Cart.objects.get(user=request.user)

        cart.products.add(product)
        return Response({'Result': 'Success'})


class CartDeleteProduct(APIView):
    http_method_names = ['post']
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        product = get_object_or_404(Product, pk=pk)
        cart = Cart.objects.get(user=request.user)

        cart.products.remove(product)
        return Response({'Result': 'Success'})

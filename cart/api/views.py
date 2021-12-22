from rest_framework.generics import ListAPIView, GenericAPIView, UpdateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.api.serializers import CartListProductsSerializer, CartSerializer
from cart.models import Cart
from product.models import Product
from product.utils import get_products_price, get_sum_price


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
        serializer = self.serializer_class(instance=self.get_object(), data=request.data, context=self.get_serializer_context())
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


class CartUpdateSumPrice(APIView):
    http_method_names = ['get']
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        cart = Cart.objects.filter(user=request.user).only('id').first()
        products = Product.objects.filter(cart=cart).only('weight', 'carat', 'wage', 'stone_price')
        products_price = get_products_price(products)

        new_price = {}
        for inx, product in enumerate(products):
            new_price.update({product.name: products_price[inx]})

        sum_price = get_sum_price(products_price)
        cart.sum_prices = sum_price
        cart.save(update_fields=['sum_prices'])

        result = {'Updated price': new_price, 'Cart sum price': cart.sum_prices}
        return Response(result, 200)


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

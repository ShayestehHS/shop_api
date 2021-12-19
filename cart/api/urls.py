from django.urls import path

from cart.api import views

app_name = 'cart'

urlpatterns = [
    path('', views.RetrieveCart.as_view(), name="home"),
    path('list/', views.CartListProducts.as_view(), name="list"),
    path('add/<int:pk>/', views.CartAddProduct.as_view(), name="add"),
    path('delete/<int:pk>/', views.CartDeleteProduct.as_view(), name="delete"),
]

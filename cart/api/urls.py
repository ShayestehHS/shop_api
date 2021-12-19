from django.urls import path

from cart.api import views

app_name = 'cart'

urlpatterns = [
    path('add/', views.CartAddProduct.as_view(), name="add"),
    path('add/<int:pk>/', views.CartAddProductURL.as_view(), name="add-by-url"),
    path('list/', views.CartListProduct.as_view(), name="list"),
]

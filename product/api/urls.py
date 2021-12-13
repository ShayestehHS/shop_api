from django.urls import path

from product.api import views

app_name = 'product'

urlpatterns = [
    path('create/', views.ProductCreate.as_view(), name='create'),
    path('retrieve/<int:pk>/', views.ProductRetrieve.as_view(), name='retrieve'),
]

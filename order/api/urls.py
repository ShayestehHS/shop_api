from django.urls import path

from order.api import views

app_name = 'order'

urlpatterns = [
    path('', views.OrderListAPIView.as_view(), name='list'),
    path('create/', views.OrderCreateAPIView.as_view(), name='create'),
    path('pay/', views.PaymentAPIView.as_view(), name='pay'),
    path('verify/', views.VerifyAPIView.as_view(), name='zp_verify'),
]

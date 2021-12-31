from django.urls import include, path

from accounts.api import views

urlpatterns = [
    path('', include('dj_rest_auth.urls')),
    path('registration/', include('dj_rest_auth.registration.urls')),
    path('registration/resend-email/', views.CustomResendEmailVerificationView.as_view(), name='rest_resend_email'),
    path('registration/account-confirm-email/<str:key>/', views.CustomConfirmEmailView.as_view(), name="account_confirm_email"),
]

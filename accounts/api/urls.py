from django.urls import include, path

from accounts.api import views

urlpatterns = [
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('dj_rest-auth/registration/resend-email/', views.CustomResendEmailVerificationView.as_view(), name='rest_resend_email'),
    path('dj-rest-auth/registration/account-confirm-email/<str:key>/', views.CustomConfirmEmailView.as_view(), name="account_confirm_email"),

]

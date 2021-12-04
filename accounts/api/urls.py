from django.urls import include, path

from dj_rest_auth.registration.views import VerifyEmailView

from accounts.api import views

app_name = 'accounts'

urlpatterns = [
    path('<int:pk>/', views.UserProfile.as_view(), name='user-profile'),

    path('dj_rest-auth/registration/resend-email/', views.CustomResendEmailVerificationView.as_view(), name='rest_resend_email'),
    path('dj_rest-auth/verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('dj-rest-auth/registration/account-confirm-email/<str:key>/', views.CustomConfirmEmailView.as_view(), name="account_confirm_email"),
    path('dj_rest-auth/', include('dj_rest_auth.urls')),
    path('dj_rest-auth/registration/', include('dj_rest_auth.registration.urls')),
]

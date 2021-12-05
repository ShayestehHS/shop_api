import requests
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from allauth.account.views import ConfirmEmailView
from allauth.account.models import EmailAddress
from dj_rest_auth.registration.views import ResendEmailVerificationView
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from accounts.tasks import task_send_confirmation_email

User = get_user_model()


class CustomConfirmEmailView(ConfirmEmailView):
    def get(self, *args, **kwargs):
        post_data = {'key': self.kwargs.get('key')}
        url = self.request.build_absolute_uri(reverse('verify-email'))
        response = requests.post(url, data=post_data)

        if response.status_code != status.HTTP_200_OK:
            messages.error(self.request, 'Your key is not valid')
            return redirect('home')

        messages.error(self.request, 'Your key is not valid')
        user = get_user_model().objects.filter(email=self.request.user.email).only('id')
        user_page = reverse('rest_user_details', args=[user.id])
        return redirect(user_page)


class CustomResendEmailVerificationView(ResendEmailVerificationView):
    queryset = EmailAddress.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = EmailAddress.objects\
            .filter(**serializer.validated_data)\
            .only('id', 'verified')

        if not email.exists():
            raise ValidationError("Account does not exist")
        email = email.first()
        if email.verified:
            raise ValidationError("Account is already verified")

        task_send_confirmation_email.delay(email.id)
        return Response({'detail': _('ok')}, status=status.HTTP_200_OK)

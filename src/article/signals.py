from django.dispatch import receiver
from django_comments_xtd.signals import should_request_be_authorized


@receiver(should_request_be_authorized)
def my_callback(sender, comment, request, **kwargs):
    return bool(request.user and request.user.is_authenticated)

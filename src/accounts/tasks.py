from allauth.account.models import EmailAddress
from celery import shared_task


@shared_task(ignore_result=True)
def task_send_confirmation_email(email_id: int):
    try:
        email = EmailAddress.objects.get(id=email_id)
        email.send_confirmation()
        return True
    except:
        return False
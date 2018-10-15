import pdb

from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.db.models.signals import post_save
from django.dispatch import receiver

from vhc_project import settings
from . models import Branch


@receiver(post_save, sender=Branch)
def send_branch_created_mail(sender, instance, created, **kwargs):

    pdb.set_trace()

    try:
        subject = "Branch creation successfully"
        email_msg = "This is test message for creation of branches"
        email = EmailMessage(subject, email_msg, settings.EMAIL_HOST_USER, [instance.email])
        email.send()

    except User.DoesNotExist:
        pass

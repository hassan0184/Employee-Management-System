from distutils.command.clean import clean
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Employee
from django.core.mail import EmailMessage
from .forms import EmployeeModelForm
import os
@receiver(post_save, sender=Employee)
def send_mail_to_repoter(sender, instance, created, **kwargs):
    if created:
        msg = EmailMessage(
            from_email='internal@zweidevs.com',
            to=[instance.email],
        )
        msg.template_id = "d-2e1b77ca99d34085a77ba01fe2621670"
        msg.dynamic_template_data = {
            "name":instance.first_name,
            "email": instance.email,
            "password": EmployeeModelForm.get(),
            "front-end-url":os.environ.get("ZI_FRONTEND_URL")
        }
        msg.send(fail_silently=False)
        return

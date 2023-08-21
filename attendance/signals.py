from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ExtraTime
from django.core.mail import EmailMessage

@receiver(post_save, sender=ExtraTime)
def send_mail_to_repoter(sender, instance, created, **kwargs):
    if created:
        msg = EmailMessage(
            from_email='internal@zweidevs.com',
            to=[instance.report_to.email],
        )
        msg.template_id = "d-8d70af44994c458ab93c680b198ca10c"
        msg.dynamic_template_data = {
            "name": instance.employee.get_name(),
            "hours": instance.number_of_hours,
            "date": instance.date.strftime('%d/%m/%Y'),
        }
        msg.send(fail_silently=False)
        return
    else:
        msg = EmailMessage(
            from_email='internal@zweidevs.com',
            to=[instance.employee.email],
        )
        msg.template_id = "d-4bb6ecd335fe4ec585739b2f15e01351"
        msg.dynamic_template_data = {
            "name": instance.report_to.get_name(),
            "hours": instance.number_of_hours,
            "date": instance.date.strftime('%d/%m/%Y'),
        }
        msg.send(fail_silently=False)
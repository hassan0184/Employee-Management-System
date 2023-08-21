from django.core.management.base import BaseCommand
from employee.models import Employee

class Command(BaseCommand):
    def handle(self, *args, **options):
        if not Employee.objects.filter(email='admin@zweidevs.com').exists():
            try:
                Employee.objects.create_superuser('admin@zweidevs.com', 'Test@1234')
            except:
                pass
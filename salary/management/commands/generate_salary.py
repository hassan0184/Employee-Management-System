from django.core.management.base import BaseCommand
from employee.models import Employee
import datetime 
from salary.utils import compute_salary
from salary.models import Salary


class Command(BaseCommand):
    def handle(self, *args, **options):
        compute_salary()
        return

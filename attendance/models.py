from django.db import models
from employee.models import Employee
from general.models import BaseModel
from .choices import ExtraTimeStatus


class ExtraTime(BaseModel):
    """Model to log extra time"""
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE,related_name='employee')
    times = models.IntegerField(default=1)
    number_of_hours = models.IntegerField(default=1)
    notes = models.TextField(blank=True)
    date = models.DateField()
    report_to=models.ForeignKey(Employee, on_delete=models.CASCADE,related_name='reported_by')
    status = models.CharField(choices=ExtraTimeStatus.choices,default=ExtraTimeStatus.PENDING, max_length=1)


    def __str__(self):
        """return name of employee"""
        return self.employee.first_name + " " + self.employee.last_name
from django.db import models
from employee.models import Employee
from general.models import BaseModel
from .choices import AllowanceType, DeductionType
# Create your models here.


class SalaryAllowance(BaseModel):
    """Model to create officer"""
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    type = models.CharField(choices=AllowanceType.choices, default=AllowanceType.OTHER, max_length=15)
    amount = models.IntegerField()
    notes = models.TextField(blank=True)
    for_month_year = models.DateField()

    def __str__(self):
        """return first_name of officer"""
        return self.employee.first_name + " " + self.employee.last_name


class SalaryDeduction(BaseModel):
    """Model to create officer"""
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    type = models.CharField(choices=DeductionType.choices, default=DeductionType.OTHER, max_length=15)
    amount = models.IntegerField()
    notes = models.TextField(blank=True)
    for_month_year = models.DateField()
    
    def __str__(self):
        """return first_name of officer"""
        return self.employee.first_name + " " + self.employee.last_name


class Salary(BaseModel):
    """Model to create officer"""
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    monthly_salary = models.IntegerField()
    computed_salary=models.IntegerField(null=True)
    notes = models.TextField(blank=True)
    for_month_year = models.DateField()
    
    def __str__(self):
        """return first_name of officer"""
        return self.employee.first_name + " " + self.employee.last_name
    class Meta:
        verbose_name_plural = "Salaries"


class DeductionAmount(BaseModel):
    """Model for set amount of latecomers as well as absent employees"""
    late_comers_amount = models.IntegerField()
    absent_amount=models.IntegerField(null=True)
   
    def __str__(self):
        """return late_comers_amount and DeductionAmount of officer"""
        return 'Late Comers Fine:{} Absent Fine:{}'.format(self.late_comers_amount,self.absent_amount)
    class Meta:
        verbose_name_plural = "Deduction Amount Employees"
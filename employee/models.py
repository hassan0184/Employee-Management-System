import uuid
from .validators import validate_file_size
from django.contrib.auth.models import AbstractUser
from django.db import models
from .choices import EmployeeStatus,AttendenceStatus
from .managers import UserManager
from lunch.models import LunchMenu
from django.shortcuts import redirect

# Create your models here.


class Employee(AbstractUser):
    """Model to create Employee"""
    email = models.EmailField(max_length=40, unique=True)
    employee_number = models.UUIDField( default = uuid.uuid4, editable = False)
    attendence_id = models.IntegerField(blank=True,null=True,unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    cnic = models.CharField(max_length=100)
    account_number = models.CharField(max_length=100, blank=True, null=True)
    base_salary = models.IntegerField(blank=True, default=0)
    status = models.CharField(default=EmployeeStatus.PROBATION, choices=EmployeeStatus.choices,  max_length=15)
    designation = models.CharField(max_length=25, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    city = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=50, blank=True)
    address = models.TextField(blank=True)
    lunch_menu = models.ManyToManyField(LunchMenu, related_name='for_employee',blank=True)
    profile_image = models.ImageField(upload_to='images',null=True,blank=True,validators=[validate_file_size])  
    requested_salary_slip=models.FileField(upload_to='monthly salaries',null=True,blank=True)
    time_slot=models.CharField(max_length=50, blank=True, null=True)
    cinic_front=models.FileField(blank=True, null=True,upload_to='cnic front',validators=[validate_file_size])
    cinic_back=models.FileField(blank=True, null=True,upload_to='cnic back',validators=[validate_file_size])
    checkin_time=models.TimeField(blank=True,null=True,editable = False)
    username = None
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'
    objects = UserManager()
    class Meta:
         verbose_name = "Employee"
    def __str__(self):
        """return email of user"""
        return self.email
    def get_name(self):
        """return name of user"""
        return self.first_name + " " + self.last_name
    def save(self, *args, **kwargs):
                self.checkin_time=self.time_slot[0:2]
                super(Employee, self).save(*args, **kwargs)


class CheckIn(models.Model):
    status = models.CharField(default=AttendenceStatus.ABSENT, choices=AttendenceStatus.choices,  max_length=15)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    checkin_time = models.TimeField(blank=True,null=True)
    checkin_date= models.DateField(blank=True,null=True)
    class Meta:
        verbose_name_plural = "Attendence"
    def __str__(self):
        return 'CheckIn of {} at {}'.format(self.employee.first_name+ " " + self.employee.last_name, self.checkin_time)
    
    


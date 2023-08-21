from django.db import models
from employee.models import Employee



class Todo(models.Model):
    title = models.CharField(max_length=100)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    description= models.TextField()
    created_at = models.DateTimeField('Created', auto_now_add=True)
    isCompleted = models.BooleanField(default=False)

class Annocument(models.Model):
    annoucment = models.TextField(blank=True,null=True)
    date=models.DateField(blank=True,null=True)
    def __str__(self):
        return str(self.date)
    class Meta:
         verbose_name = "Company Annoument"
    

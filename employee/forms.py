from django.forms import ModelForm
from django import forms
from datetime import datetime, timedelta
from lunch.models import LunchMenu
from .models import Employee
from django.contrib.auth.hashers import make_password
from .utils import validate_password_admin
from django.core.exceptions import ValidationError


class EmployeeModelForm(ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'

    
    def clean(self):
        global USER_PASSWORD
        data = self.cleaned_data
        if not Employee.objects.filter(email=data['email']): 
          if validate_password_admin(data['password']) == True:
             USER_PASSWORD=data['password']
             data['password'] = make_password(data['password'])
          else:
                 raise ValidationError("Follow the password set rules")



    def __init__(self, *args, **kwargs):
        input_dt = datetime.today().date()
        day_num = input_dt.strftime("%d")
        first = input_dt - timedelta(days=int(day_num) - 1)
        end = first.replace(day=28) + timedelta(days=4)
        end = end - timedelta(end.day)
        forms.ModelForm.__init__(self, *args, **kwargs)
        self.fields['lunch_menu'].queryset = LunchMenu.objects.filter(date__gte=first,date__lte=end)
    def get():
        return USER_PASSWORD

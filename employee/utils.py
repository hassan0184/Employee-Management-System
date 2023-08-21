from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from .models import Employee
from django.core.mail import EmailMultiAlternatives
from django.core.mail import EmailMessage
from decouple import config
import json
import datetime
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.models import update_last_login



def login_employee(request, format=None):
    email = request.data.get("email")
    password = request.data.get("password")
    email = email.lower()
    data = login_employee_using_email_password(email, password)
    return Response(data, status=status.HTTP_200_OK)

    
def login_employee_using_email_password(email, password, throw_exception=True, is_password_encrypted=False):
    if email is None:
        raise ValidationError('Email should not be empty')
    if password is None:
        raise ValidationError('Password should not be empty')
    try:
            Employee.objects.get(email=email)

    except Employee.DoesNotExist:
            raise ValidationError('Employee does not exist')

    user = authenticate(email=email, password=password)
    if user is not None:
        return get_access_and_refresh_token_for_employee(user)
    if throw_exception:
        raise ValidationError('Invalid login credentials')
    return False


def get_access_and_refresh_token_for_employee(employee):
    if employee is not None:
        
        refresh = RefreshToken.for_user(employee)
        data = {
        'refresh_token': str(refresh),
        'access_token': str(refresh.access_token),
        'last_login':employee.last_login
         }
        employee.last_login=datetime.datetime.now()
        employee.save()
        return data
             



def send_welcome_email(firstname,email,absurl):


    """
    Send an email for forget password'
    """

    first_name=firstname
    reciever_email=email
    
    msg = EmailMessage(
        from_email= config('FROM_EMAIL'),
        to=[reciever_email],
    )
    msg.template_id = config('TEMPLATE_ID_OTP')
    
    msg.dynamic_template_data = {
        'name': firstname,
        'absurl': absurl
        
    }
    msg.send(fail_silently=False)


def validate_password(passwd):
    
    SpecialSym =['$', '@', '#', '%',  '/', '[', '`', '!','^', '&', '*', '(',')', '_', '+', '-','=', ']', '{', '}',';', ':',  '|','<', '>', '?', '~']
   
    if not any(char in SpecialSym for char in passwd):
         
        return False

    else:
        return True

def validate_password_admin(passwd):
    
    SpecialSym =['$', '@', '#', '%',  '/', '[', '`', '!','^', '&', '*', '(',')', '_', '+', '-','=', ']', '{', '}',';', ':',  '|','<', '>', '?', '~']
    if len(passwd)>=8 and len(passwd)<=10:
      if not any(char in SpecialSym for char in passwd):
         
        return False

      else:
        return True
    else:
        return False

        
  
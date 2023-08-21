
from rest_framework import serializers
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.core.exceptions import ValidationError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .models import Employee,CheckIn
from .utils  import validate_password
from rest_framework.response import Response
from rest_framework import status

class CheckInDetailSerializer(serializers.ModelSerializer):
     class Meta:
        model=CheckIn
        fields=["employee", "checkin_time", "checkin_date", "status"]


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Employee
        fields=["id", "employee_number", "first_name", "last_name", "status", "phone", "date_joined", "email", "address", 'cnic', 'designation','profile_image','city','country','state','time_slot', 'account_number']

class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    redirect_url = serializers.CharField(max_length=500, required=False)

    class Meta:
        fields = ['email']


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=8, max_length=10, write_only=True)
  

    def validate(self, attrs):

            password = attrs.get('password')
            token = self.context['token']
            uidb64 =self.context['uid']
            id = force_str(urlsafe_base64_decode(uidb64))
            user = Employee.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)
            else:
              if validate_password(password)==True:
               user.set_password(password)
               user.save()
               return user

              else:
                 raise serializers.ValidationError("Follow the password set rules")
                
      
        
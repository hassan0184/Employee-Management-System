from django.http import HttpResponse
import pandas as pd
from django.shortcuts import redirect
from django.shortcuts import render
from employee.serializers import EmployeeSerializer
from rest_framework.views import APIView
from .utils import login_employee,send_welcome_email
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView,UpdateAPIView
from employee.models import Employee,CheckIn
from rest_framework import status
from rest_framework.response import Response
from decouple import config
import calendar
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from .serializers import SetNewPasswordSerializer,CheckInDetailSerializer
from django.http import HttpResponsePermanentRedirect
from decouple import config
from .utils  import validate_password
from django.contrib.auth.hashers import  check_password
from django.views.generic.base import TemplateView
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
import datetime
from datetime import date,datetime, timedelta
from django.contrib import messages
import pathlib
from dateutil import parser
from django.db.models import Q


class EmployeeLoginView(APIView):

    def post(self, request, format=None):
        return login_employee(request)


class AllEmployeeAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        return Employee.objects.filter(is_superuser=False, is_active=True)

class CheckInDetailView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CheckInDetailSerializer

    def get_queryset(self):
        input_dt=date.today()
        next_month = input_dt.replace(day=28) + timedelta(days=4)
        res = next_month - timedelta(days=next_month.day)
        return CheckIn.objects.filter(
            employee=self.request.user,
            checkin_date__gte=input_dt.replace(day=1),
            checkin_date__lte=res,
        ).order_by('checkin_date')
class EmployeeAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeSerializer

    def get_object(self):
        return Employee.objects.get(id=self.request.user.id)


class EmployeeForgetPassword(APIView):
    

    def post(self, request):
         
         email = request.data.get("email")
 
         if not Employee.objects.filter(email=email).first():
            return Response(data={'success': False, 'message': 'This email doesnot exist in our system'}, status=status.HTTP_400_BAD_REQUEST)
         
         user=Employee.objects.get(email=email)
         uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
         token = PasswordResetTokenGenerator().make_token(user)
         current_site =config('HOST')
         absurl = '{}/{}/{}'.format(current_site, uidb64, token)
         send_welcome_email(user.first_name,email,absurl)
         return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)
class SetNewPasswordAPIView(APIView):
    
    def patch(self, request,**kwargs):
        
        serializer=SetNewPasswordSerializer(data=request.data,context={'uid':kwargs['uidb64'],'token':kwargs['token']})
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)


class PasswordTokenCheckAPI(APIView):
    

    def get(self, request, uidb64, token):


        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = Employee.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user,token):
                return Response({'success':False,'message': 'Token is not valid, please request a new one'}, status= status.HTTP_400_BAD_REQUEST)

            return Response({'success':True,'message': 'credentials valid'}, status=status.HTTP_200_OK)


        except DjangoUnicodeDecodeError as identifier:
            
                if not PasswordResetTokenGenerator().check_token(user):
                   return Response({'success':False,'message': 'Token is not valid, please request a new one'}, status=status.HTTP_400_BAD_REQUEST)


class EmployeeUpdatePassword(APIView):
    permission_classes = [IsAuthenticated]
    def patch(self, request):
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        confirm_password = request.data.get("confirm_password")
        
        user= Employee.objects.filter(id=self.request.user.id).first()
        checkpassword=check_password(old_password,user.password)
        if checkpassword == True:
            if new_password != confirm_password:
                return Response({'success':False,'message': 'New Password and Confirm Password Must Be Same'}, status=status.HTTP_400_BAD_REQUEST)
            elif old_password == new_password and old_password == confirm_password:
                return Response({'success':False,'message': 'New Password is Same as Old Password '}, status=status.HTTP_400_BAD_REQUEST)
            else:
                if len(new_password)>=8 and len(new_password)<=10 and validate_password(new_password) == True:
                  user.set_password(new_password)
                  user.save()
                  return Response({'success':True,'message': 'Password Updated SuccessFully'}, status=status.HTTP_200_OK)
                else:
                     return Response({'success':False,'message': 'Follow the password set rules'}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'success':False,'message': 'You Entered Wrong Current Password'}, status=status.HTTP_400_BAD_REQUEST)


def UpdatePasswordByAdmin(request):
     message=request.POST.get('user_id')
     return render(request, 'change_password.html',{"id":message})


class ChangePasswordByAdmin(APIView):
    def post(self,request):
         id=request.POST.get('user_id')
         new_password=request.POST.get('new-password')
         user=Employee.objects.filter(id=id).first()
         user.password=make_password(new_password)
         user.save()
         return redirect(config('HOST')+'admin/employee/employee/')

def handle_attendencefile(request):
    doc=request.FILES
    if doc:
      attendence_file = doc['fileInput']
      file_extension = pathlib.Path(attendence_file.name).suffix
      if file_extension == '.csv':
        try:
            df = pd.read_csv(attendence_file)
            today_date=0
            for ind in df.index:
                if df['Status'][ind] == 'C/In':
                    date_time=parser.parse(df['Date/Time'][ind])
                    today_date=date_time
                    get_object=Employee.objects.filter(attendence_id=df['No.'][ind]).first()
                    if get_object:
                        if not CheckIn.objects.filter(employee=get_object,checkin_date= date_time.date()).exists():
                                if get_object.checkin_time.replace(minute=30) >= date_time.time():
                                    CheckIn.objects.create(employee=get_object, checkin_time=date_time.time(),checkin_date= date_time.date(),status='Present') 
                                elif get_object.checkin_time.replace(minute=30) < date_time.time():
                                    CheckIn.objects.create(employee=get_object, checkin_time=date_time.time(),checkin_date= date_time.date(),status='Late') 
                        else:
                            continue
            employee_set=Employee.objects.filter(~Q(id__in=CheckIn.objects.filter(checkin_date=today_date.date()).values_list("employee_id")),is_superuser=False, is_active=True)   
            for get_object in employee_set:
                CheckIn.objects.create(employee=get_object,checkin_date= today_date.date(),status='Absent') 
        except:
            messages.error(request,'CSV file is not with proper data')
            return redirect("/admin/employee/checkin/")

        return redirect("/admin/employee/checkin/")
      else:
        messages.error(request,'Please Upload file in CSV format')
        return redirect("/admin/employee/checkin/")
    else:
        messages.error(request,'You have not uploaded anyfile')
        return redirect("/admin/employee/checkin/")

        

        

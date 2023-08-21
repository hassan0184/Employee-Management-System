from django.core.files import File
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from employee.models import Employee
from .models import Salary, SalaryAllowance, SalaryDeduction
from .serializers import SalarySerializer
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.db.models import Sum
from rest_framework import status
from .utils import generate_pdf,generate_salary
import inflect
import os
from datetime import datetime, timedelta, date
from weasyprint import HTML
from django.views.decorators.csrf import csrf_exempt





class SalaryAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        month = int(self.request.query_params.get("month", datetime.now().month))
        year = int(self.request.query_params.get("year",datetime.now().year))
        start_date = date(year, month,1)
        end = start_date.replace(day=28) + timedelta(days=4)
        end = end - timedelta(end.day)
        return Salary.objects.filter(employee=self.request.user, for_month_year__gte=start_date, for_month_year__lte=end)
    
    serializer_class=SalarySerializer

class GeneratePdf(APIView):
    permission_classes = [IsAuthenticated]
   
    def get(self, request):
        """Fetch All Notes By Officer"""
        try:
          ALLOWANCE_DICT={}
          DEDUCTION_DICT={}

          employee =self.request.user
          month = int(request.query_params.get("month", datetime.now().month))
          year = int(request.query_params.get("year", datetime.now().year))
          start_date = date(year, month,1)
          end = start_date.replace(day=28) + timedelta(days=4)
          end = end - timedelta(end.day)
          user_obj=Employee.objects.get(id=employee.id)
          salary_allowance = SalaryAllowance.objects.filter(employee=self.request.user, for_month_year__gte = start_date, for_month_year__lte=end)
          salary_deduction = SalaryDeduction.objects.filter(employee=self.request.user, for_month_year__gte = start_date, for_month_year__lte=end)

          for obj in salary_allowance:
            if obj.type in ALLOWANCE_DICT:
              value=obj.amount + ALLOWANCE_DICT[obj.type]
              ALLOWANCE_DICT.update({obj.type:value})
            else:
              ALLOWANCE_DICT[obj.type]=obj.amount
          for obj in salary_deduction:
            if obj.type in DEDUCTION_DICT:
              value=obj.amount + DEDUCTION_DICT[obj.type]
              DEDUCTION_DICT.update({obj.type:value})
            else:
              DEDUCTION_DICT[obj.type]=obj.amount

          NET_SALARY=user_obj.base_salary+sum(ALLOWANCE_DICT.values())-sum(DEDUCTION_DICT.values())
          p = inflect.engine()
          NET_SALARY_WORDS=p.number_to_words(NET_SALARY)
          temp_name = "general/templates/" 
          salary_template = "salary " + str(employee.id) + " of " + str(month) + "-" + str(year) + ".html"
          open(temp_name + salary_template, "w").write(render_to_string('salary.html', {'employee_detail': user_obj,'obj_allowance':ALLOWANCE_DICT,'obj_deduction':DEDUCTION_DICT,'NET_SALARY':NET_SALARY,'NET_SALARY_WORDS':NET_SALARY_WORDS}))
          HTML(temp_name + salary_template).write_pdf(str(employee.id)+'.pdf')
          user_obj.requested_salary_slip=File(open(str(employee.id)+'.pdf', 'rb'))
          user_obj.save()
          os.remove(str(employee.id)+'.pdf')
          os.remove(temp_name + salary_template)
          return Response({'salary_report': user_obj.requested_salary_slip.url}, status=status.HTTP_200_OK)
        except Exception as e:
          return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def GenerateAllEmployeePdfByAdmin(request):

      startdate=request.POST['startdate']
      enddate=request.POST['enddate']
      cheque=request.POST['cheque']
      user_obj=Employee.objects.filter(is_superuser=False, is_active=True)
      return generate_pdf(startdate,enddate,cheque,user_obj) 


class GenerateAllEmployeeSalaryByAdmin(APIView):
  
  def get(self, request):
      input_dt = datetime.today().date()
      day_num = input_dt.strftime("%d")
      startdate = input_dt - timedelta(days=int(day_num) - 1)
      end = startdate.replace(day=28) + timedelta(days=4)
      enddate = end - timedelta(end.day)
      user_obj=Employee.objects.filter(is_superuser=False, is_active=True)
      return generate_salary(startdate,enddate,user_obj,request) 
     
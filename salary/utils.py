import datetime
import inflect
from employee.models import Employee,CheckIn
from django.db.models import Q
from .models import SalaryDeduction,SalaryAllowance
from attendance.models import ExtraTime
from salary.choices import AllowanceType,DeductionType
from attendance.choices import ExtraTimeStatus
from employee.choices import AttendenceStatus
from salary.models import Salary,DeductionAmount
from django.db.models import Sum
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus.tables import Table,TableStyle,colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph,Spacer
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import redirect
from os import environ


NUMBER_OF_WORKING_DAYS=22
NUMBER_OF_HOURS=8
LUNCH_AMOUNT=150

def compute_salary():
    employees = Employee.objects.filter(is_superuser=False, is_active=True)
    month = datetime.datetime.now().month
    year = datetime.datetime.now().year
    for employee in employees:
        compute_salary_allowance(employee, month, year)
        compute_salary_deduction(employee, month, year)

def compute_salary_for_specific(start_date,end_date):
    employees = Employee.objects.filter(is_superuser=False, is_active=True)
    month = datetime.datetime.now().month
    year = datetime.datetime.now().year
    for employee in employees:
        compute_salary_allowance_for_specific(employee, month, year,start_date,end_date)
        compute_salary_deduction_for_specific(employee, month, year,start_date,end_date)

def compute_salary_deduction_for_specific(employee,month,year,start_date,end_date):
   
    for_month_year = datetime.date(year, month,1)
    start = datetime.date(year, month,1)
    start = start - datetime.timedelta(days=1)
    start = datetime.date(start.year, start.month, 25)
    end = datetime.date(year, month,1) + datetime.timedelta(days=23)
    lunch_count = Employee.objects.filter(id=employee.id,lunch_menu__date__gte=start_date,lunch_menu__date__lte=end_date).count()
    total = lunch_count * LUNCH_AMOUNT
    late_comers_count=  CheckIn.objects.filter(employee=employee,status=AttendenceStatus.LATE,checkin_date__gte=start_date,checkin_date__lte=end_date).count()
    deduction_amount=DeductionAmount.objects.all().values("late_comers_amount")
    total_late_comers_fine=deduction_amount[0]['late_comers_amount'] * int(late_comers_count)
    absent_count=  CheckIn.objects.filter(employee=employee,status=AttendenceStatus.ABSENT,checkin_date__gte=start_date,checkin_date__lte=end_date).count()
    deduction_amount=DeductionAmount.objects.all().values("absent_amount")
    total_absent_fine=deduction_amount[0]['absent_amount']* int(absent_count)
    
    if not SalaryDeduction.objects.filter(employee=employee, for_month_year=for_month_year,type=DeductionType.LUNCH).exists():
      if total != 0:
         SalaryDeduction.objects.create(employee=employee,type=DeductionType.LUNCH,amount=total,for_month_year=for_month_year)
    else:
        salary_deduction = SalaryDeduction.objects.get(employee=employee, for_month_year=for_month_year, type=DeductionType.LUNCH)
        salary_deduction.type =DeductionType.LUNCH
        salary_deduction.amount = total
        salary_deduction.save()

        
    if not SalaryDeduction.objects.filter(employee=employee, for_month_year=for_month_year,type=DeductionType.LATE).exists():
      if total_late_comers_fine != 0:
        SalaryDeduction.objects.create(employee=employee,type=DeductionType.LATE,amount=total_late_comers_fine,for_month_year=for_month_year)
    else:
        salary_deduction = SalaryDeduction.objects.get(employee=employee, for_month_year=for_month_year, type=DeductionType.LATE)
        salary_deduction.type =DeductionType.LATE
        salary_deduction.amount = total_late_comers_fine
        salary_deduction.save()

    if not SalaryDeduction.objects.filter(employee=employee, for_month_year=for_month_year,type=DeductionType.ABSENT).exists():
      if total_absent_fine != 0:
        SalaryDeduction.objects.create(employee=employee,type=DeductionType.ABSENT,amount=total_absent_fine,for_month_year=for_month_year)
    else:
        salary_deduction = SalaryDeduction.objects.get(employee=employee, for_month_year=for_month_year, type=DeductionType.ABSENT)
        salary_deduction.type =DeductionType.ABSENT
        salary_deduction.amount = total_absent_fine
        salary_deduction.save()


def compute_salary_allowance_for_specific(employee, month, year,start_date,end_date):


    total_extra_hours = 0
    for_month_year = datetime.date(year, month,1)
    start = datetime.date(year, month,1)
    start = start - datetime.timedelta(days=1)
    start = datetime.date(start.year, start.month, 25)
    end = datetime.date(year, month,1) + datetime.timedelta(days=23)
    extra_hours = ExtraTime.objects.filter(employee = employee, date__gte = start_date, date__lte=end_date, status=ExtraTimeStatus.APPROVED)
    
    for obj in extra_hours:
        total_extra_hours += obj.number_of_hours*obj.times*employee.base_salary/NUMBER_OF_WORKING_DAYS/NUMBER_OF_HOURS

    if not SalaryAllowance.objects.filter(employee=employee, for_month_year=for_month_year,  type=AllowanceType.EXTRA_HOURS).exists():
      if total_extra_hours != 0:
        SalaryAllowance.objects.create(employee=employee, type=AllowanceType.EXTRA_HOURS ,amount=total_extra_hours, for_month_year=for_month_year) 
    else:
        salary_allowance = SalaryAllowance.objects.get(employee=employee, for_month_year=for_month_year, type=AllowanceType.EXTRA_HOURS)
        salary_allowance.type = AllowanceType.EXTRA_HOURS
        salary_allowance.amount = total_extra_hours
        salary_allowance.save()

def compute_salary_deduction(employee,month,year):
   
    for_month_year = datetime.date(year, month,1)
    start = datetime.date(year, month,1)
    start = start - datetime.timedelta(days=1)
    start = datetime.date(start.year, start.month, 25)
    end = datetime.date(year, month,1) + datetime.timedelta(days=23)
    lunch_count = Employee.objects.filter(id=employee.id,lunch_menu__date__gte=start,lunch_menu__date__lte=end).count()
    total = lunch_count * LUNCH_AMOUNT
    late_comers_count=  CheckIn.objects.filter(employee=employee,status=AttendenceStatus.LATE,checkin_date__gte=start,checkin_date__lte=end).count()
    deduction_amount=DeductionAmount.objects.all().values("late_comers_amount")
    total_late_comers_fine=deduction_amount[0]['late_comers_amount'] * int(late_comers_count)
    absent_count=  CheckIn.objects.filter(employee=employee,status=AttendenceStatus.ABSENT,checkin_date__gte=start,checkin_date__lte=end).count()
    deduction_amount=DeductionAmount.objects.all().values("absent_amount")
    total_absent_fine=deduction_amount[0]['absent_amount']* int(absent_count)
    

    
    if not SalaryDeduction.objects.filter(employee=employee, for_month_year=for_month_year,type=DeductionType.LUNCH).exists():
      if total != 0:
        SalaryDeduction.objects.create(employee=employee,type=DeductionType.LUNCH,amount=total,for_month_year=for_month_year)
    else:
        salary_deduction = SalaryDeduction.objects.get(employee=employee, for_month_year=for_month_year, type=DeductionType.LUNCH)
        salary_deduction.type =DeductionType.LUNCH
        salary_deduction.amount = total
        salary_deduction.save()

    if not SalaryDeduction.objects.filter(employee=employee, for_month_year=for_month_year,type=DeductionType.LATE).exists():
      if total_late_comers_fine != 0:
        SalaryDeduction.objects.create(employee=employee,type=DeductionType.LATE,amount=total_late_comers_fine,for_month_year=for_month_year)
    else:
        salary_deduction = SalaryDeduction.objects.get(employee=employee, for_month_year=for_month_year, type=DeductionType.LATE)
        salary_deduction.type =DeductionType.LATE
        salary_deduction.amount = total_late_comers_fine
        salary_deduction.save()

    if not SalaryDeduction.objects.filter(employee=employee, for_month_year=for_month_year,type=DeductionType.ABSENT).exists():
      if total_absent_fine != 0:
        SalaryDeduction.objects.create(employee=employee,type=DeductionType.ABSENT,amount=total_absent_fine,for_month_year=for_month_year)
    else:
        salary_deduction = SalaryDeduction.objects.get(employee=employee, for_month_year=for_month_year, type=DeductionType.ABSENT)
        salary_deduction.type =DeductionType.ABSENT
        salary_deduction.amount = total_absent_fine
        salary_deduction.save()

def compute_salary_allowance(employee, month, year):


    total_extra_hours = 0
    for_month_year = datetime.date(year, month,1)
    start = datetime.date(year, month,1)
    start = start - datetime.timedelta(days=1)
    start = datetime.date(start.year, start.month, 25)
    end = datetime.date(year, month,1) + datetime.timedelta(days=23)
    extra_hours = ExtraTime.objects.filter(employee = employee, date__gte = start, date__lte=end, status=ExtraTimeStatus.APPROVED)
    for obj in extra_hours:
        total_extra_hours += obj.number_of_hours*obj.times*employee.base_salary/NUMBER_OF_WORKING_DAYS/NUMBER_OF_HOURS

    if not SalaryAllowance.objects.filter(employee=employee, for_month_year=for_month_year,  type=AllowanceType.EXTRA_HOURS).exists():
        if total_extra_hours != 0:
           SalaryAllowance.objects.create(employee=employee, type=AllowanceType.EXTRA_HOURS ,amount=total_extra_hours, for_month_year=for_month_year) 
    else:
        salary_allowance = SalaryAllowance.objects.get(employee=employee, for_month_year=for_month_year, type=AllowanceType.EXTRA_HOURS)
        salary_allowance.type = AllowanceType.EXTRA_HOURS
        salary_allowance.amount = total_extra_hours
        salary_allowance.save()
    
def generate_pdf(start_date,end,cheque,user_obj):
      compute_salary_for_specific(start_date,end)
 
      my_path='{}/my_pdf_byadmin.pdf'.format(settings.BASE_DIR)
      my_doc=SimpleDocTemplate(my_path, pagesize=A4)
      elements = []
      styles=getSampleStyleSheet()
      style = [

('ALIGN', (1, 0), (-1, -1), 'CENTER'),

   ]
      column1Heading = "No"
      column2Heading = "Names"
      column3Heading = "Account Number"
      column4Heading = "CNIC"
      column5Heading = "Amount"
      i=1
      
      data = [[column1Heading,column2Heading,column3Heading,column4Heading,column5Heading]]
      TOTAL_SALARY=0
      for obj in user_obj:
        TOTAL_DEDUCTION=0
        TOTAL_ALLOWANCE=0
        allowance_obj = SalaryAllowance.objects.filter(employee_id=obj.id, for_month_year__gte=start_date, for_month_year__lte=end).values('employee__email').annotate(amount=Sum('amount'))
        if allowance_obj :
          TOTAL_ALLOWANCE=allowance_obj[0].get('amount')
        deduction_obj = SalaryDeduction.objects.filter(employee_id=obj.id, for_month_year__gte=start_date, for_month_year__lte=end).values('employee__email').annotate(amount=Sum('amount'))
        
        if deduction_obj :
          TOTAL_DEDUCTION=deduction_obj[0].get('amount')

        TOTAL=obj.base_salary + TOTAL_ALLOWANCE-TOTAL_DEDUCTION
        if obj.account_number:
          TOTAL_SALARY =TOTAL_SALARY+TOTAL

        
            
        if not Salary.objects.filter(employee=obj,for_month_year__gte=start_date,for_month_year__lte=end).exists():
               Salary.objects.create(employee=obj, monthly_salary=obj.base_salary,computed_salary=TOTAL, for_month_year=end)
               
         
        else:
              salary = Salary.objects.get(employee=obj,for_month_year__gte=start_date,for_month_year__lte=end)
              salary.monthly_salary=obj.base_salary
              salary.computed_salary=TOTAL
              salary.for_month_year=end
              salary.save()

        if obj.account_number:
         data.append([i, obj.first_name.capitalize() +' '+ obj.last_name.capitalize(),obj.account_number,obj.cnic,TOTAL])
         i=i+1
        else:
          continue


      data.append(["The Total Amount In Rs       ","         ","         ", "        ",TOTAL_SALARY])
     
     
      tableThatSplitsOverPages = Table(data, [3 * cm, 3 * cm], repeatRows=1, style = style)
      tblStyle = TableStyle()
      for line in range(1,7):
        tblStyle.add ('LINEBEFORE', (line,0), (line,i-1), 0.5, colors.black)
                      
                           

      tblStyle.add('LINEBELOW',(0,0),(-1,i-1),0.5,colors.black)
      tblStyle.add('BOX',(0,0),(-1,-1),1,colors.black)
      tblStyle.add('BACKGROUND',(0,0),(4,0),colors.lightblue)
      tblStyle.add('BACKGROUND',(0,1),(-1,-1),colors.white)
      tableThatSplitsOverPages.setStyle(tblStyle)
      elements.append(tableThatSplitsOverPages)





      my_Style=ParagraphStyle('My Para style',fontSize=10)
      p1=Paragraph('''<BR/><BR/><BR/><BR/><BR/>The Branch Manager,<BR/>\
          Meezan Bank,<BR/><BR/> \
	        <b>Subject: Fund transfer voucher, Account: '''+str(environ.get('ZI_ACCOUNT_NUMBER'))+''' <BR/>\
          Rs:'''+str(TOTAL_SALARY) +'''/- Cheque:'''+str(cheque) +'''</b> <BR/><BR/> \
          Dear Sir,<BR/> \
	        Please note this letter is a formal request for funds transfers from my company account
          to the accounts mentioned below. <BR/><BR/><BR/><BR/>\
          ''',my_Style)

      c = canvas.Canvas(my_path, pagesize=A4)
      width,height=A4 
      p1.wrapOn(c,300,50)
      p1.drawOn(c,width-550,height-150)
      my_doc.build([
      p1,
      tableThatSplitsOverPages])
      
      file = open('{}/my_pdf_byadmin.pdf'.format(settings.BASE_DIR), 'rb')
      response = HttpResponse(file, content_type='application/pdf')
      response['Content-Disposition'] = 'attachment;filename=bank_salary_document.pdf'
      return response
  






  

def generate_salary(start_date,end,user_obj,request):
      compute_salary()
 
      
    
      TOTAL_SALARY=0
      for obj in user_obj:
        TOTAL_DEDUCTION=0
        TOTAL_ALLOWANCE=0
        allowance_obj = SalaryAllowance.objects.filter(employee_id=obj.id, for_month_year__gte=start_date, for_month_year__lte=end).values('employee__email').annotate(amount=Sum('amount'))
        if allowance_obj :
          TOTAL_ALLOWANCE=allowance_obj[0].get('amount')
        deduction_obj = SalaryDeduction.objects.filter(employee_id=obj.id, for_month_year__gte=start_date, for_month_year__lte=end).values('employee__email').annotate(amount=Sum('amount'))
        
        if deduction_obj :
          TOTAL_DEDUCTION=deduction_obj[0].get('amount')

        TOTAL=obj.base_salary + TOTAL_ALLOWANCE-TOTAL_DEDUCTION
        TOTAL_SALARY =TOTAL_SALARY+TOTAL

        
            
        if not Salary.objects.filter(employee=obj,for_month_year__gte=start_date,for_month_year__lte=end).exists():
               Salary.objects.create(employee=obj, monthly_salary=obj.base_salary,computed_salary=TOTAL, for_month_year=end)
               continue
               
               
         
        else:
              salary = Salary.objects.get(employee=obj,for_month_year__gte=start_date,for_month_year__lte=end)
              salary.monthly_salary=obj.base_salary
              Salary.computed_salary=TOTAL
              salary.for_month_year=end
              salary.save()
              continue

      return redirect(request.META.get('HTTP_REFERER'))

     
     
     
                           

      





     
    
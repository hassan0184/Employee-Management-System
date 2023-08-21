import wget
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus.tables import Table,TableStyle,colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph,Spacer
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4,landscape,letter
from reportlab.lib.styles import  getSampleStyleSheet
from reportlab.platypus import Paragraph
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import redirect
from .models import LunchMenu
from employee.models import Employee
from reportlab.lib.units import inch
from django.db.models import Count
import  zipfile
from io import BytesIO



def generate_pdf(start_date,end,week_name):
      
      my_path='{}/my_menu_pdf_byadmin.pdf'.format(settings.BASE_DIR)
      pagesize = (14 * inch, 14 * inch)
      my_doc=SimpleDocTemplate(my_path, pagesize=landscape(A4))
      elements = []
      styles=getSampleStyleSheet()
      style = [

('ALIGN', (1, 0), (-1, -1), 'CENTER'),

   ]  
      column1Heading = "No"
      column2Heading = "Name"

      i=1
      COLUMN_LIST={}
      Employees_queryset=Employee.objects.filter(is_superuser=False, is_active=True)
      count_lunch=Employee.objects.filter(is_superuser=False, is_active=True,lunch_menu__date__gte=start_date,lunch_menu__date__lte=end).values('lunch_menu__date','lunch_menu__dish__name').annotate(total=Count('lunch_menu__date')).order_by('lunch_menu__date')
      data = [[column1Heading,column2Heading]]
      for column in count_lunch:
         COLUMN_LIST[column['lunch_menu__date']]=column['lunch_menu__dish__name']
      column_list_new_value = list(COLUMN_LIST.items())
      column_iterate=0
      for iterate in column_list_new_value:
         data[0].extend([str(column_list_new_value[column_iterate][0]) + "\n" + str(column_list_new_value[column_iterate][1])])
         column_iterate=column_iterate+1

      data[0].extend(["Employee" + "\n" + " Count"])
      for employee in Employees_queryset:
         data.append([i,str(employee.first_name)+" "+str(employee.last_name)])
         Employee_Lunch_Set=employee.lunch_menu.filter(date__gte=start_date,date__lte=end).order_by('date')
         employee_month_count=0
         for check in column_list_new_value:
               if Employee_Lunch_Set.filter(dish__name=check[1]).exists():
                  data[i].append("Yes")
                  employee_month_count=employee_month_count+1
               else:
                  data[i].append("No")
         data[i].append(employee_month_count)
         i=i+1

      data.append(["Daily Count "])
      data[i].append(" ")
      for dish_date in count_lunch:
         data[i].append(dish_date['total'])
      i=i+1

      tableThatSplitsOverPages = Table(data, colWidths=[0.9*inch] + [None] * (len(data[0]) - 1), repeatRows=1, style = style)
      tblStyle = TableStyle()
      for line in range(1,column_iterate+3):

        tblStyle.add ('LINEBEFORE', (line,0), (line,i-1), 0.5, colors.black)
                      
                           
      tblStyle.add('LINEBELOW',(0,0),(-1,i-1),0.5,colors.black)
      tblStyle.add('BOX',(0,0),(-1,-1),1,colors.black)
      tblStyle.add('BACKGROUND',(0,0),(column_iterate+3,0),colors.lightblue)
      tblStyle.add('BACKGROUND',(0,1),(-1,-1),colors.white)
      tableThatSplitsOverPages.setStyle(tblStyle)
      elements.append(tableThatSplitsOverPages)


      my_doc.build([
      tableThatSplitsOverPages])
      
      
      file = open('{}/my_menu_pdf_byadmin.pdf'.format(settings.BASE_DIR), 'rb')
      response = HttpResponse(file, content_type='application/pdf')
      response['Content-Disposition'] = 'attachment;filename='+week_name+ '.pdf'
      return response

def generate_pdf_foradmin(start_date,end):
      
      my_path='{}/my_menu_pdf_byadmin.pdf'.format(settings.BASE_DIR)
      my_doc=SimpleDocTemplate(my_path, pagesize=A4)
      elements = []
      styles=getSampleStyleSheet()
      style = [

('ALIGN', (1, 0), (-1, -1), 'CENTER'),

   ]
      column1Heading = "No"
      column2Heading = "Date"
      column3Heading= "Dish"
      column4Heading = "Count"


      i=1
      count_lunch=Employee.objects.filter(is_superuser=False, is_active=True,lunch_menu__date__gte=start_date,lunch_menu__date__lte=end).values('lunch_menu__date','lunch_menu__dish__name').annotate(total=Count('lunch_menu__date')).order_by('lunch_menu__date')
      data = [[column1Heading,column2Heading,column3Heading,column4Heading]]
           
      for dish_date in count_lunch:
         
         data.append([i,dish_date['lunch_menu__date'], dish_date['lunch_menu__dish__name'],dish_date['total']])
         i=i+1
       
      tableThatSplitsOverPages = Table(data, colWidths=[1.9*inch] + [None] * (len(data[0]) - 1), repeatRows=1, style = style)
      tblStyle = TableStyle()
      for line in range(1,7):
        tblStyle.add ('LINEBEFORE', (line,0), (line,i-1), 0.5, colors.black)
                      
                           
      tblStyle.add('LINEBELOW',(0,0),(-1,i-1),0.5,colors.black)
      tblStyle.add('BOX',(0,0),(-1,-1),1,colors.black)
      tblStyle.add('BACKGROUND',(0,0),(4,0),colors.lightblue)
      tblStyle.add('BACKGROUND',(0,1),(-1,-1),colors.white)
      tableThatSplitsOverPages.setStyle(tblStyle)
      elements.append(tableThatSplitsOverPages)


      my_doc.build([
      tableThatSplitsOverPages])
      
      file = open('{}/my_menu_pdf_byadmin.pdf'.format(settings.BASE_DIR), 'rb')
      response = HttpResponse(file, content_type='application/pdf')
      response['Content-Disposition'] = 'attachment;filename=Lunch_Menu.pdf'
      return response

def zipFiles(files):
        outfile = BytesIO()   
        with zipfile.ZipFile(outfile, 'w') as zf:
            for n, f in enumerate(files):
                zf.writestr('week'+str(n+1)+'.pdf'.format(n), f.getvalue())
        return outfile.getvalue()
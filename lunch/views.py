from employee.models import Employee
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from .serializers import LunchSerializer
from datetime import timedelta
from datetime import datetime
from .models import LunchMenu,Dish
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
import datetime
import calendar
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from common_utilities.response_template import get_response_template
from .utils import generate_pdf,generate_pdf_foradmin,zipFiles
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import FileResponse





class ListMenuAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        month = int(self.request.query_params.get("month", datetime.datetime.now().month))
        year = int(self.request.query_params.get("year", datetime.datetime.now().year))        
        start = datetime.date(year, month,1)
        end = start.replace(day=28) + datetime.timedelta(days=4)
        end = end - datetime.timedelta(end.day)
        end = datetime.date(end.year, end.month,25)
        last_month = start - datetime.timedelta(days=1)
        start = datetime.date(last_month.year, last_month.month,26)
        return LunchMenu.objects.filter(date__gte = start, date__lte=end).order_by('date')
    
    serializer_class=LunchSerializer


class LunchMenuOptInAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user=request.user
        lunch_menu = request.data.get("lunch_menu")

        opt_in_model = Employee.objects.get(id=user.id)
        if opt_in_model:
            month = datetime.datetime.now().month
            year = datetime.datetime.now().year
            start = datetime.date(year, month,1)
            end = start.replace(day=28) + datetime.timedelta(days=4)
            end = end - datetime.timedelta(end.day)
            end = datetime.date(end.year, end.month,25)
            last_month = start - datetime.timedelta(days=1)
            start = datetime.date(last_month.year, last_month.month,26)
            current_lunch_menu = list(LunchMenu.objects.filter(date__gte = start, date__lte=end).values_list('id', flat=True))
            current_lunch_menu = list(set(current_lunch_menu) - set(lunch_menu))
            opt_in_model.lunch_menu.remove(*current_lunch_menu)
            opt_in_model.lunch_menu.add(*lunch_menu)
            opt_in_model.save()
        response_template = get_response_template()
        return Response(response_template)

@csrf_exempt
def GenerateMenuPdfByAdmin(request):
      startdate=request.POST['startdate']
      enddate=request.POST['enddate']
      return generate_pdf_foradmin(startdate,enddate) 

@csrf_exempt
def GenerateMenuPdfDaily(request):
            current_month=request.POST['month']
            input_dt = datetime.date(int(current_month[0:4]),int(current_month[5:7] ), 1)
            day_num = input_dt.strftime("%d")
            startdate = input_dt - timedelta(days=int(day_num) - 1)
            end = startdate.replace(day=28) + timedelta(days=4)
            enddate = end - timedelta(end.day)
            response_list=[]
            day=7
            current_month_days=calendar.monthrange(input_dt.year, input_dt.month)[1]
            for i in range(4):
                
                if i ==3 :
                    remainaing_days=current_month_days-startdate.day
                    enddate=startdate.replace(day=startdate.day+remainaing_days)
                    resp=generate_pdf(startdate,enddate,"week" + str(i+1))
                    response_list.append(resp)
                    break
                else:
                    enddate=startdate.replace(day=startdate.day+day)
                    resp=generate_pdf(startdate,enddate,"week" + str(i+1))
                    response_list.append(resp)
                    startdate=enddate.replace(day=enddate.day+1)

            zipped_file = zipFiles(response_list)
            response = HttpResponse(zipped_file, content_type='application/octet-stream')
            response['Content-Disposition'] = 'attachment; filename=lunchmenu.zip' 
            return  response
from rest_framework.generics import CreateAPIView,ListAPIView, UpdateAPIView,DestroyAPIView
from rest_framework import response
from .serializers import ExtraTimeSerializer,ExtraTimeCalendarSerializer
from .models import ExtraTime
from rest_framework.permissions import IsAuthenticated
from employee.models import Employee
import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status





class AddExtraTimeAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ExtraTimeSerializer


class UpdateExtraTimeAPIView(UpdateAPIView):
    queryset = ExtraTime.objects.all()
    serializer_class = ExtraTimeSerializer

    def get_queryset(self):
        return ExtraTime.objects.all();


class ExtraTimeCalendarAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        month = int(self.request.query_params.get("month", datetime.datetime.now().month))
        year = int(self.request.query_params.get("year", datetime.datetime.now().year))
        start = datetime.date(year, month,1)
        end = start.replace(day=28) + datetime.timedelta(days=4)
        end = end - datetime.timedelta(end.day)
        return ExtraTime.objects.filter(employee=self.request.user, date__gte = start, date__lte=end)
    
    serializer_class=ExtraTimeCalendarSerializer


class ExtraTimeRequestAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        month = int(self.request.query_params.get("month", datetime.datetime.now().month))
        year = int(self.request.query_params.get("year", datetime.datetime.now().year))
        start = datetime.date(year, month,1)
        end = start.replace(day=28) + datetime.timedelta(days=4)
        end = end - datetime.timedelta(end.day)
        return ExtraTime.objects.filter(report_to=self.request.user, date__gte = start, date__lte=end)
    
    serializer_class=ExtraTimeCalendarSerializer

class DeleteTimeAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request,pk):
        user=request.user
        obj = ExtraTime.objects.get(employee=user,id=pk)
        obj.delete()
        return Response(data={'success': True, 'message': 'Deleted Successfully'}, status=status.HTTP_200_OK)
    
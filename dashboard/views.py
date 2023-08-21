from urllib import request
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import response
from .serializers import DashBoardSerializer, TodoListRelatedSerializer
from .models import Todo
import datetime
from rest_framework.permissions import IsAuthenticated
from employee.models import Employee
from datetime import date


class TodoListViewsList(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DashBoardSerializer

    def get_queryset(self):
        user = Employee.objects.filter(id=self.request.user.id)
        return user

    def get_serializer_context(self):
        month = int(self.request.query_params.get(
            "month", datetime.datetime.now().month))
        year = int(self.request.query_params.get(
            "year", datetime.datetime.now().year))
        today = date.today()
        start = datetime.date(year, month, 1)
        end = start.replace(day=28) + datetime.timedelta(days=4)
        end = end - datetime.timedelta(end.day)
        return {'user': self.request.user, 'start': start, 'end': end, 'today_date': today}


class TodoListRelatedViews(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TodoListRelatedSerializer

    def get_queryset(self):
        results = Todo.objects.filter(employee=self.request.user)
        return results


class TodoListViewsCreate(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TodoListRelatedSerializer

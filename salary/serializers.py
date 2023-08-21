from bdb import Breakpoint
from rest_framework import serializers
from .models import Salary, SalaryAllowance, SalaryDeduction
import datetime
from django.db.models import Sum,Count


class SalaryAllowanceSerializer(serializers.ModelSerializer):

     class Meta:
        model=SalaryAllowance
        fields=['id', 'amount','type']

class SalaryDeductionSerializer(serializers.ModelSerializer):
     class Meta:
        model=SalaryAllowance
        fields=['id', 'amount', 'type']

class SalarySerializer(serializers.ModelSerializer):

    allowances = serializers.SerializerMethodField(read_only=True)
    deductions = serializers.SerializerMethodField(read_only=True)

    def get_allowances(self, obj):
        month = int(self.context["request"].query_params["month"])
        year = int(self.context["request"].query_params["year"])
        start = datetime.date(year, month, 1)
        end = start.replace(day=28) + datetime.timedelta(days=4)
        end = end - datetime.timedelta(end.day)
        data = SalaryAllowance.objects.filter(employee= self.context["request"].user, for_month_year__gte=start, for_month_year__lte=end).values('type').annotate(amount=Sum('amount'))

        return SalaryAllowanceSerializer(data, many=True).data

    def get_deductions(self, obj):
        month = int(self.context["request"].query_params["month"])
        year = int(self.context["request"].query_params["year"])
        start = datetime.date(year, month, 1)
        end = start.replace(day=28) + datetime.timedelta(days=4)
        end = end - datetime.timedelta(end.day)
        data = SalaryDeduction.objects.filter(employee= self.context["request"].user, for_month_year__gte=start, for_month_year__lte=end).values('type').annotate(amount=Sum('amount'))
        return SalaryAllowanceSerializer(data, many=True).data

    class Meta:
        model=Salary
        fields=['id', 'monthly_salary','for_month_year', 'allowances', 'deductions']
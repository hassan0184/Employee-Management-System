from rest_framework import serializers
from .models import ExtraTime
from employee.serializers import EmployeeSerializer


class ExtraTimeSerializer(serializers.ModelSerializer):

    class Meta:
        model=ExtraTime
        fields=['id','number_of_hours','report_to','notes','date', 'employee', 'status']
        extra_kwargs = {
            "employee": {"read_only": True},
        }

    def create(self, validated_data):
        validated_data["employee"] = self.context["request"].user
        return super().create(validated_data)

class ExtraTimeCalendarSerializer(serializers.ModelSerializer):

    employee = EmployeeSerializer(read_only=True)

    class Meta:
        model=ExtraTime
        fields=['id', 'number_of_hours','date','status','notes', 'employee']

    
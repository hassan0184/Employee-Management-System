from employee.models import Employee
from rest_framework import serializers
from .models import LunchMenu,Dish


class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model=Dish
        fields=['name']


class LunchSerializer(serializers.ModelSerializer):

    dish = DishSerializer(read_only=True)
    employee_opt_in = serializers.SerializerMethodField(read_only=True)

    def get_employee_opt_in(self, obj):
        
        data = Employee.objects.filter(id= self.context["request"].user.id, lunch_menu=obj)
        if data.count() == 0:
            return False
        else:
            return True

    class Meta:
        model=LunchMenu
        fields=['id', 'dish','date', 'employee_opt_in']
    

    
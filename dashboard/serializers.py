from employee.models import Employee
from rest_framework import serializers
from datetime import date
from lunch.models import LunchMenu
from .models import Todo,Annocument
from attendance.models import ExtraTime
from attendance.choices import ExtraTimeStatus
from employee.models import CheckIn
from django.db.models import Sum



class StickyNotesSerializer(serializers.ModelSerializer):
    class Meta:
      model=Todo
      fields=['title','description','created_at','isCompleted'] 

class DashBoardSerializer(serializers.ModelSerializer):
    extra_hours = serializers.SerializerMethodField(method_name="get_extra_hours")
    today_lunch = serializers.SerializerMethodField(method_name="get_today_lunch")
    sticky_notes = serializers.SerializerMethodField(method_name="get_sticky_notes")
    company_anoucments=serializers.SerializerMethodField(method_name="get_company_anoucments")
    checkin_details=serializers.SerializerMethodField(method_name="get_checkin_details")



    def get_extra_hours(self, obj):
        data = ExtraTime.objects.filter(employee= self.context['user'],date__gte=self.context['start'],date__lte= self.context['end'], status=ExtraTimeStatus.APPROVED).values('employee__email',).annotate(number_of_hours=Sum('number_of_hours'))
        if data.count() == 0:
            return 0
        else:
            return data[0].get('number_of_hours')


    def get_today_lunch(self, obj):
        data=Employee.objects.filter(id=obj.id,lunch_menu__date=self.context['today_date']).values('lunch_menu__dish__name')     
        if not data:
            user_lunch=LunchMenu.objects.filter(date=self.context['today_date']).first()
            if user_lunch:
              return {"status":False,"dish":user_lunch.dish.name}
            else:
                return {}
        else:
            return {"status":True,"dish":data[0].get('lunch_menu__dish__name')}
    
    def get_sticky_notes(self,obj):
        data=Todo.objects.filter(employee=obj).values('id','title','description','created_at','isCompleted')
        return data
    def get_company_anoucments(self,obj):
        data=Annocument.objects.filter(date=self.context['today_date']).values("annoucment")
        return data
    
    def get_checkin_details(self,obj):
        data=CheckIn.objects.filter(employee=obj,checkin_date=self.context['today_date']).values('checkin_time','checkin_date','status')
        return data


    class Meta:
        model=Employee
        fields=['id','extra_hours','company_anoucments','today_lunch','sticky_notes','checkin_details']





class TodoListRelatedSerializer(serializers.ModelSerializer):

    class Meta:
        model=Todo
        fields=['title','description' ]

    def create(self, validated_data):
         validated_data["employee"] = self.context["request"].user
         return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.title=validated_data['title']
        instance.description=validated_data['description']
        instance.save()
        return instance
    
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Employee,CheckIn
from django.shortcuts import render
from django.contrib.auth.admin import UserAdmin
from .forms import EmployeeModelForm
from django.shortcuts import redirect
from django.urls import reverse
from django_object_actions import DjangoObjectActions
from django import forms
from django.contrib import messages
from django.http import HttpResponse
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter,ChoiceDropdownFilter,SimpleDropdownFilter
from rangefilter.filters import DateRangeFilter



class EmployeeAdminDisplay(admin.ModelAdmin):
    form = EmployeeModelForm
    def firstname_and_lastname(obj,obj1):
     return "%s %s" % (obj1.first_name, obj1.last_name)
    def address_city_state_country(obj,obj1):
     return "%s %s %s %s" % (obj1.address,obj1.city,obj1.state,obj1.country)
   
    list_display=['__str__','attendence_id','firstname_and_lastname','designation','cnic','account_number','phone','address_city_state_country','date_joined','time_slot','checkin_time','base_salary','profile_image']
    ordering = ('attendence_id',)
    filter_horizontal = ('lunch_menu',)
    change_password_form = ('password',)

    def get_exclude(self, request, obj=None):
     if obj:
        return ["password","checkin_time"]
     else:
        return []

    change_form_template = "change_form.html"

    def change_view(self, request, *args, **kwargs ):
       extra_context = {}
       id=kwargs['object_id']
       return super().change_view(request,id,extra_context={"id":id})
   
   #  def save_model(self, request, obj, form, change):
        
   #      if Employee.objects.filter(attendence_id=obj.attendence_id).exists():
   #          return messages.error(request,'The Employee with Attendence Id {} already exists'.format(obj.attendence_id))
   #      else:
   #          super(EmployeeAdminDisplay, self).save_model(request, obj, form, change)

class CheckInAdminDisplay(DjangoObjectActions,admin.ModelAdmin):
   list_display=['employee','status','checkin_time','checkin_date']
   list_filter = (
        ('checkin_date', DateRangeFilter),
        ("employee",RelatedDropdownFilter),
        ("status",ChoiceDropdownFilter),
        
    )
  
   def employee(self, obj):
        return obj.employee.get_name()

   def upload_checkin_file(modeladmin, request, queryset):
        return render(request,
                      'change_list.html',
                      context={})

   changelist_actions = ('upload_checkin_file',)

  


admin.site.register(CheckIn,CheckInAdminDisplay)
admin.site.register(Employee,EmployeeAdminDisplay)

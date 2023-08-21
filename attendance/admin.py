from django.contrib import admin
from .models import ExtraTime
from django_admin_listfilter_dropdown.filters import  RelatedDropdownFilter,ChoiceDropdownFilter
from rangefilter.filters import DateRangeFilter


# Register your models here.
class ExtraHoursAdminDisplay(admin.ModelAdmin):
    list_display = ("id","employee","date","report_to","notes", "number_of_hours")
    list_filter = (
        ('date', DateRangeFilter),
        ("employee",RelatedDropdownFilter),
        ("status",ChoiceDropdownFilter)
        
    )
    

admin.site.register(ExtraTime,ExtraHoursAdminDisplay)

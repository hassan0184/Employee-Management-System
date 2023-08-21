from django.contrib import admin
from django.shortcuts import render
from .models import SalaryAllowance, SalaryDeduction, Salary,DeductionAmount
from django_object_actions import DjangoObjectActions
from .utils import compute_salary
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter,ChoiceDropdownFilter,SimpleDropdownFilter
from rangefilter.filters import DateRangeFilter
from django.shortcuts import redirect



class SalaryAllowanceAdmin(admin.ModelAdmin):
    list_display=['id','amount','employee','notes','type']
    list_filter = (
        ('for_month_year', DateRangeFilter),
        ("employee",RelatedDropdownFilter),
        ("type",ChoiceDropdownFilter)
        
    )
    
admin.site.register(SalaryAllowance,SalaryAllowanceAdmin)
class SalaryDeductionAdmin(admin.ModelAdmin):
    list_display=['id','amount','employee','notes','type']
    list_filter = (
        ('for_month_year', DateRangeFilter),
        ("employee",RelatedDropdownFilter),
        ("type",ChoiceDropdownFilter)
        
    )
admin.site.register(SalaryDeduction,SalaryDeductionAdmin)

@admin.register(Salary)
class UserAdmin(DjangoObjectActions, admin.ModelAdmin):
    list_display = ("employee", "monthly_salary","computed_salary")

    def generate_pdf(modeladmin, request, queryset):
        return render(request,
                      'generate_pdf_admin.html',
                      context={})

    def generate_salary(modeladmin, request, queryset):
        return redirect('/salary/generate-salary-all-employee-byadmin/')
                    

    changelist_actions = ('generate_pdf','generate_salary')
    
@admin.register(DeductionAmount) 
class DeductionAmountADmin(admin.ModelAdmin):
    list_display=['late_comers_amount','absent_amount']
    def has_add_permission(self, request): 
        count = DeductionAmount.objects.all().count()
        if count == 0:
            return True
        return False
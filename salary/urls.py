from django.urls import path
from .views import SalaryAPIView, GeneratePdf,GenerateAllEmployeePdfByAdmin,GenerateAllEmployeeSalaryByAdmin
from django.urls import path, reverse_lazy
from django.views.generic.base import RedirectView

urlpatterns = [
    
    path('',SalaryAPIView.as_view(),name="list-salary"),
    path('pdf/', GeneratePdf.as_view()), 
    path('generate-pdf-all-employee-byadmin', GenerateAllEmployeePdfByAdmin,name="generate-pdf-all-employee-byadmin"), 
    path('generate-salary-all-employee-byadmin/', GenerateAllEmployeeSalaryByAdmin.as_view(),name="generate_salary_admin"), 
    
]
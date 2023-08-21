from django.urls import path
from .views import EmployeeAPIView, EmployeeLoginView, AllEmployeeAPIView,EmployeeForgetPassword,SetNewPasswordAPIView,PasswordTokenCheckAPI,EmployeeUpdatePassword,UpdatePasswordByAdmin,ChangePasswordByAdmin,handle_attendencefile,CheckInDetailView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    
    path('login',EmployeeLoginView.as_view(),name="employee-login"),
    path('me',EmployeeAPIView.as_view(),name="employee-me"),
    path('checkin-details/',CheckInDetailView.as_view(),name="checkin-details"),
    path('',AllEmployeeAPIView.as_view(),name="employee-all"),
    path('update-password/',EmployeeUpdatePassword.as_view(),name="update_password"),
    path('request-reset-password/',EmployeeForgetPassword.as_view(),name="employee-all"),
    path('password-reset-complete/<str:uidb64>/<str:token>/', SetNewPasswordAPIView.as_view(),
         name='password-reset-complete'),
    path('password-reset-check-token/<str:uidb64>/<str:token>/',PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('token-refresh/',TokenRefreshView.as_view(),name="token-refresh"),
    path('update-password-by-admin',UpdatePasswordByAdmin,name="update-password-by-admin"),
    path('change_password_by_admin',ChangePasswordByAdmin.as_view(),name="change-password-by-admin"),
    path('upload_attendence_file', handle_attendencefile, name='upload_attendence_file'),
]
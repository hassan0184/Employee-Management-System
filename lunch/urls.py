from django.urls import path
from .views import ListMenuAPIView, LunchMenuOptInAPIView,GenerateMenuPdfByAdmin,GenerateMenuPdfDaily


urlpatterns = [
    path('',ListMenuAPIView.as_view(),name="list-lunch-menu"),
    path('opt-in',LunchMenuOptInAPIView.as_view(),name="lunch-menu-opt-in"),
    path('GenerateMenuPdfMonthly',GenerateMenuPdfByAdmin,name="GenerateMenuPdfMonthly"),
    path('GenerateMenuPdfDaily',GenerateMenuPdfDaily,name="GenerateMenuPdfDaily")


]

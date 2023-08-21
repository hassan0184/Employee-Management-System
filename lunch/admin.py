from django.contrib import admin
from django.shortcuts import redirect
from .models import LunchMenu,Dish
from rangefilter.filters import DateRangeFilter
from django.shortcuts import render
from django_object_actions import DjangoObjectActions



class DishAdminDisplay(admin.ModelAdmin):
    list_display = ("id","name")

@admin.register(LunchMenu)
class LunchMenuAdminDisplay(DjangoObjectActions, admin.ModelAdmin):
    list_display = ("id","date", "dish","notes")
    list_filter=(
        ("date",DateRangeFilter),
        )
    ordering = ('date',)

    def Monthly_Lunch_Count(modeladmin, request, queryset):
        return render(request,
                      'generate_menu_pdf_admin.html',
                      context={})
    def Daily_Lunch_Detail(modeladmin, request, queryset):  
        return render(request,
                      'generate_menu_daily_pdf.html',
                      context={})

    changelist_actions = ('Monthly_Lunch_Count','Daily_Lunch_Detail')


admin.site.register(Dish, DishAdminDisplay)
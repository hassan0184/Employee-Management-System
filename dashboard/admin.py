from django.contrib import admin
from .models import Todo,Annocument
from django.contrib import messages
from django.shortcuts import redirect

class AnnocumentAdminView(admin.ModelAdmin):
    list_display=['date']
    def has_add_permission(self, request): 
        count = Annocument.objects.all().count()
        if count == 0:
            return True
        return False


admin.site.register(Annocument,AnnocumentAdminView)






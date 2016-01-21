from django.contrib import admin

from .models import AdminContent,Pserson
# Register your models here.

class AdminList(admin.ModelAdmin):
    list_display = ('title','pub_date','update_time')

class Personadmin(admin.ModelAdmin):
    list_display = ('full_name',)

admin.site.register(AdminContent,AdminList)
admin.site.register(Pserson,Personadmin)
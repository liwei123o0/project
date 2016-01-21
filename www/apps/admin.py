# -*- coding: utf-8 -*-
#! /usr/bin/env python
from django.contrib import admin

from .models import AdminContent,Pserson
# Register your models here.

class AdminList(admin.ModelAdmin):
    #列表显示
    list_display = ('title','content','pub_date','update_time')

    #后台内容搜索功能
    search_fields = ('title','content')
    def get_search_results(self, request, queryset, search_term):
        queryset,use_distinct = super(AdminList,self).get_search_results(request,queryset,search_term)
        try:
            search_term_as_int = int(search_term)
            queryset |= self.model.objects.filter(age=search_term_as_int)
        except:
            pass
        return queryset,use_distinct
#根据不同人显示不同信息，权限查看
class MyAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super(MyAdmin,self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(author=request.user)

class Personadmin(admin.ModelAdmin):
    list_display = ('full_name',)

admin.site.register(AdminContent,AdminList)
admin.site.register(Pserson,Personadmin)
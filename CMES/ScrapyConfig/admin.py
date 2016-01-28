# -*- coding: utf-8 -*-
#! /usr/bin/env python
from django.contrib import admin
from .models import LanMu,WenZhang

# Register your models here.

class LanMuAdmin(admin.ModelAdmin):
    list_display = ('name','urlLM','nav_display',)

class WenZhangAdmin(admin.ModelAdmin):
    list_display = ('title','author','published','pub_date','update_time',)

admin.site.register(LanMu,LanMuAdmin)
admin.site.register(WenZhang,WenZhangAdmin)
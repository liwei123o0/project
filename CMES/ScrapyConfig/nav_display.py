# -*- coding: utf-8 -*-
#! /usr/bin/env python

#添加导航栏全显示上下文
from .models import LanMu

list_nav = LanMu.objects.filter(nav_display=True)

def nav_display(request):
    return {'list_nav':list_nav}
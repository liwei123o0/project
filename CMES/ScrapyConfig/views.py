# -*- coding: utf-8 -*-
#! /usr/bin/env python

from django.shortcuts import render
from .models import LanMu,WenZhang
# Create your views here.

def home(request):

    list_nav = LanMu.objects.filter(nav_display=True)

    return render(request,'home.html',{"list_nav":list_nav})

def ListLanMu(request,lanmu_url):

    LM = LanMu.objects.get(urlLM=lanmu_url)
    return render(request,'lanmu.html',{'lanmu':LM,
                                        })
def ListWZ(request,pk):

    WZ = WenZhang.objects.get(pk=pk)

    return render(request,'wenzhang.html',{'wenzhang':WZ})

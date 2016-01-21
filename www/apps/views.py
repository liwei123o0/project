# -*- coding: utf-8 -*-
#! /usr/bin/env python
from django.shortcuts import render
from django.http import HttpResponse
from .apps import Addform
# Create your views here.

def index(request):

    if request.method == 'POST':
        form = Addform(request.POST)
        #检验数据是否合法
        if form.is_valid():
            a = form.cleaned_data['a']
            b = form.cleaned_data['b']
            return HttpResponse(str(int(a)+int(b)))
    else:
        form = Addform()
    return render(request,'index.html',{'form':form})

def add(request):
    a = request.GET['a']
    b = request.GET['b']
    return HttpResponse(str(int(a)+int(b)))


# -*- coding: utf-8 -*-
#! /usr/bin/env python
from django.shortcuts import render
from django.http import HttpResponse
from .models import Column,Article
from django.shortcuts import redirect
# Create your views here.

def index(request):
    home_display_columns = Column.objects.filter(home_display=True)
    nav_display_columns = Column.objects.filter(nav_display=True)

    columns = Column.objects.all()
    return render(request,'index.html',{
        'columns':columns,
        'home_display_columns':home_display_columns,
        'nav_display_columns':nav_display_columns,
    })

def column_detail(request,column_slug):
    column = Column.objects.get(slug=column_slug)
    return render(request,'column.html',{'column':column})

def article_detail(request,pk,article_slug):
    # article = Article.objects.get(slug=article_slug)
    #
    article = Article.objects.get(pk=pk)
    #判断网址是否修改
    if article_slug != article.slug:
        return redirect(article,permanent=True)
    return render(request,'article.html',{'article':article})


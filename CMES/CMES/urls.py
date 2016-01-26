# -*- coding: utf-8 -*-
#! /usr/bin/env python
"""CRMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
#内容记事本
from DjangoUeditor import urls as DjangoUeditor_urls
#记事本的相关设置
from  django.conf import settings

from CMS.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^ueditor/',include(DjangoUeditor_urls)),
    url(r'^$',index,name='index'),
    #生成相关网址
    url(r'^column/(?P<column_slug>[^/]+)/$',column_detail,name='column'),
    #内容根据ID及网址来生成
    url(r'^news/(?P<pk>\d+)/(?P<article_slug>[^/]+)/$',article_detail,name='article'),
    # url(r'^accounts/', include('users.urls')),
]
#有关内容编辑器上传下载等操作的改动
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns +=static(
        settings.MEDIA_URL,document_root = settings.MEDIA_ROOT
    )

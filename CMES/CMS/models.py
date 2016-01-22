# -*- coding: utf-8 -*-
#! /usr/bin/env python
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
#第三方内容编辑框
from DjangoUeditor.models import UEditorField
# Create your models here.

from django.core.urlresolvers import reverse

@python_2_unicode_compatible
class Column(models.Model):
    name = models.CharField(u'栏目名称',max_length=255)
    slug = models.CharField(u'栏目网址',max_length=255)
    intro = models.TextField(u'栏目简介',default='')

    nav_display = models.BooleanField(u'导航显示',default=False)
    home_display = models.BooleanField(u'首页显示',default=False)

    #获取网址方法
    def get_absolute_url(self):
        return reverse('column',args=(self.slug,))

    def __str__(self):
        return self.name

    class Meta:
        #站点管理名称（内容部分）
        verbose_name = u'栏目'
        #子栏目左下角显示名称（导航栏页脚部分）
        verbose_name_plural = u'栏目'
        ordering =['name']

@python_2_unicode_compatible
class Article(models.Model):
    #重点理解
    column = models.ManyToManyField(Column,verbose_name=u'归属栏目')

    title = models.CharField(u'标题',max_length=255)
    slug = models.CharField(u'网址',max_length=255,db_index=True)
    #重点理解
    author = models.ForeignKey('auth.User',blank=True,null=True,verbose_name=u'作者')
    #引入第三方内容编辑框
    content = UEditorField(u'内容',height=300,width=1000,default=u'',blank=True,
                           imagePath='uploads/images/',toolbars='besttome',
                           filePath='uploads/files/')
    published = models.BooleanField(u'正式发布',default=True)

    pub_date = models.DateTimeField(u'发表时间',auto_now=True,editable=True)
    update_time = models.DateTimeField(u'更新时间',auto_now=True,null=True)
    #动态获取网址
    def get_absolute_url(self):
        return reverse('article',args=(self.pk,self.slug,))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = u'作者'
        verbose_name_plural = u'教程'

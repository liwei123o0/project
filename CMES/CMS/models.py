# -*- coding: utf-8 -*-
#! /usr/bin/env python
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
# Create your models here.

@python_2_unicode_compatible
class Column(models.Model):
    name = models.CharField(u'栏目名称',max_length=255)
    slug = models.CharField(u'栏目网址',max_length=255)
    intro = models.TextField(u'栏目简介',default='')

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
    column = models.ManyToManyField(Column,verbose_name=u'归属栏目')

    title = models.CharField(u'标题',max_length=255)
    slug = models.CharField(u'网址',max_length=255,db_index=True)

    author = models.ForeignKey('auth.User',blank=True,null=True,verbose_name=u'作者')
    content = models.TextField(u'内容',default='',blank=True)
    published = models.BooleanField(u'正式发布',default=True)

    pub_date = models.DateTimeField(u'发表时间',auto_now=True,editable=True)
    update_time = models.DateTimeField(u'更新时间',auto_now=True,null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = u'作者'
        verbose_name_plural = u'教程'

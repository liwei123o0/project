# -*- coding: utf-8 -*-
#! /usr/bin/env python
from __future__ import unicode_literals

from django.db import models

from django.utils.encoding import python_2_unicode_compatible

# Create your models here.

@python_2_unicode_compatible
class AdminContent(models.Model):

    title = models.CharField(u'标题',max_length=256)
    content = models.TextField(u'内容')

    pub_date = models.DateTimeField(u'发表时间',auto_now=True,editable=True)
    update_time = models.DateTimeField(u'更新时间',auto_now=True,null=True)

    def __str__(self):
        return self.title

@python_2_unicode_compatible
class Pserson(models.Model):

    name = models.CharField(u'姓名',max_length=50)
    age  = models.IntegerField(u'年龄')

    fist_name = models.CharField(u'别名',max_length=50)
    last_name = models.CharField(u'全名',max_length=50)

    def my_person(self):
        return self.fist_name + ' '+self.last_name
    my_person.short_description = u'全称名字'

    full_name = property(my_person)

    def __str__(self):
        return self.age
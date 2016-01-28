# -*- coding: utf-8 -*-
#! /usr/bin/env python
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
# Create your models here.
from django.core.urlresolvers import reverse
from DjangoUeditor.models import UEditorField

@python_2_unicode_compatible
class LanMu(models.Model):
    name = models.CharField(u'栏目名称',max_length=255)
    urlLM = models.CharField(u'栏目地址',max_length=255,db_index=True)

    nav_display = models.BooleanField(u'导航显示',default=False)

    def get_absolute_url(self):
        #第一个参数对应urls.py的那么值
        return reverse('listLM',args=(self.urlLM,))

    class Meta():
        verbose_name = u'栏目'
        verbose_name_plural = u'栏目'

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class WenZhang(models.Model):

    lm = models.ManyToManyField(LanMu,verbose_name='所属栏目')
    title = models.CharField(u'标题',max_length=255)
    author = models.ForeignKey('auth.User',blank=True,null=True,verbose_name=u'作者')

    content = UEditorField(verbose_name='内容',default=u'',blank=False,
                           imagePath='uploads/images/',toolbars='besttome',
                           filePath='uploads/files/')

    pub_date = models.DateTimeField(u'发表时间',auto_now=True,editable=True)
    update_time = models.DateTimeField(u'更新时间',auto_now=True,null=True)

    published = models.BooleanField(u'正式发布',default=True)

    #动态获取网址
    def get_absolute_url(self):
        return reverse('listWZ',args=(self.pk,))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = u'作者'
        verbose_name_plural = u'文章'
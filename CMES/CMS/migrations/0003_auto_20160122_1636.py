# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-22 08:36
from __future__ import unicode_literals

import DjangoUeditor.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CMS', '0002_auto_20160122_1310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='content',
            field=DjangoUeditor.models.UEditorField(blank=True, default='', verbose_name='\u5185\u5bb9'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-27 07:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ScrapyConfig', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lanmu',
            name='nav_display',
            field=models.BooleanField(default=False, verbose_name='\u5bfc\u822a\u663e\u793a'),
        ),
    ]

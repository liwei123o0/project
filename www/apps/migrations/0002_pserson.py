# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-21 07:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pserson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='\u59d3\u540d')),
                ('age', models.IntegerField(verbose_name='\u5e74\u9f84')),
                ('fist_name', models.CharField(max_length=50, verbose_name='\u522b\u540d')),
                ('last_name', models.CharField(max_length=50, verbose_name='\u5168\u540d')),
            ],
        ),
    ]

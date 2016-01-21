from __future__ import unicode_literals

from django.apps import AppConfig

from django import forms

class AppsConfig(AppConfig):
    name = 'apps'

class Addform(forms.Form):

    a = forms.IntegerField()
    b = forms.IntegerField()


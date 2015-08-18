# -*- coding: utf-8 -*-
# ! /usr/bin/env python
from django.db import models

from dynamic_scraper.models import scraper, SchedulerRuntime
from scrapy.contrib.djangoitem import DjangoItem


class NewsWebsite(models.models):
    name = models.CharField(max_length=200)
    url = models.URLField()
    scraper = models.ForeignKey(scraper, blank=True, null=True, on_delete=models.SET_NULL)
    scraper_runtime = models.ForeignKey(SchedulerRuntime, blank=True, null=True, on_delete=models.SET_NULL)

    def __unicode__(self):
        return self.name


class Article(models.models):
    title = models.CharField(max_length=200)
    news_website = models.ForeignKey(NewsWebsite)
    description = models.TextField(blank=True)
    url = models.URLField()
    checker_runtime = models.ForeignKey(SchedulerRuntime, blank=True, null=True, on_delete=models.SET_NULL)

    def __unicode__(self):
        return self.title


class ArticleItem(DjangoItem):
    django_model = Article


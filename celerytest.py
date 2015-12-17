# -*- coding: utf-8 -*-
#! /usr/bin/env python

from celery import Celery

app = Celery('hello',broker='amqp://guest@localhost//')

@app.task
def hello():
    return 'hello word!'
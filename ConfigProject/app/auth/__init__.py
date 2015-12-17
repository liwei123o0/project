# -*- coding: utf-8 -*-
#! /usr/bin/env python

from flask import Blueprint

auth = Blueprint('auth',__name__)

from . import views
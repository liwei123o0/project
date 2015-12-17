# -*- coding: utf-8 -*-
#! /usr/bin/env python
from flask import Blueprint

main = Blueprint('main', __name__)

import views, errors

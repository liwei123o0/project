# -*- coding: utf-8 -*-
#! /usr/bin/env python

import urllib2
import json
import os
import platform
import logging

class utilsconfig():

    def read_config(self,path):
        if os.path.exists(path):
            path = os.path.abspath(path)
            if platform.system() =='Windows':
                path =path.replace('\\','/')
                path = 'file:///'+path
            else:
                path = 'file://'+path
        try:
            txt = urllib2.urlopen(path,timeout=10).read()
            print txt
            conf = json.loads(txt)
            return conf
        except Exception:
            txt = u'错误'
            return txt
# -*- coding: utf-8 -*-
#! /usr/bin/env python
import urllib2
import os
try:
    os.remove("proxy.txt")
except:
    pass
# url = " http://revx.daili666.com/ip/?tid=559196081665491&num=10&foreign=none&delay=1&protocol=http"
#
# html = urllib2.urlopen(url,timeout=10).read()
#
# html = html.replace(":","\t")
#
# with open("proxies.txt","w")as w:
#     w.write(html)
# with open("proxies.txt","r")as f:
#     fs = f.readlines()
#     for proxy in fs:
#         with open("proxy.txt","a+")as w:
#             w.write("http\t%s"% proxy.replace("\n",""))
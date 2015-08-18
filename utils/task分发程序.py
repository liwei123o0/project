# -*- coding: utf-8 -*-
#! /usr/bin/env python
import urllib2
from lxml import etree
import random
import os

req =urllib2.Request("http://10.6.2.121/conf/")
html = urllib2.urlopen(req).read()
dom = etree.HTML(html.decode("utf8"))
body = dom.xpath("//tr[@class='odd']/td/a/text()")

for conf in body:
    ips = ["124","125","126","127","128"]
    ip = random.choice(ips)

    task = "curl http://10.6.2.%s:6800/schedule.json -d \
project=example -d \
spider=example -d \
setting=CLOSESPIDER_TIMEOUT=360 -d \
config=http://10.6.2.121/conf/%s"% (str(ip),conf)
    os.system(task)
    print(task)
#! /usr/bin/env python
import urllib2
from lxml import etree
import random
import os

req =urllib2.Request("http://10.6.2.124/conf/carbj/")
html = urllib2.urlopen(req).read()
dom = etree.HTML(html.decode("utf8"))
body = dom.xpath("//tr/td/a/text()")

for conf in body:
    ips = ["125","126","127","128","129","130","131","132","134","135","136"]
    ip = random.choice(ips)

    task = "curl http://10.6.2.%s:6800/schedule.json -d \
            project=example -d \
            spider=example -d \
            setting=CLOSESPIDER_TIMEOUT=3600 -d \
            config=http://10.6.2.124/conf/carbj/%s"% (str(ip),conf)
    print task
    # os.system(task)

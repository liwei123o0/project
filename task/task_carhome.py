# -*- coding: utf-8 -*-
#! /usr/bin/env python
import urllib2
from lxml import etree
import random
import os
import time
def tast_carhome():
    try:
        req =urllib2.Request("http://10.6.2.124/conf/carhome/")
        html = urllib2.urlopen(req).read()
        dom = etree.HTML(html.decode("utf8"))
        body = dom.xpath("//tr/td/a/text()")

        for conf in body:
            ips = ["6.52","6.53","6.57","6.58","6.64","6.65","6.84","6.89",\
                "4.161","4.204","4.200","4.178","4.168","4.164","4.206",\
                "4.162","4.211","4.214","7.143","7.144","7.145","7.147",\
                "7.148","7.146","7.149","7.150","4.63","4.64","4.117",\
				"4.114","7.175","7.172","7.173","7.176","7.151","7.170",\
				"7.171","7.174"]
            ip = random.choice(ips)

            task = "curl http://10.6.%s:6800/schedule.json -d \
project=example -d \
spider=example -d \
setting=CLOSESPIDER_TIMEOUT=360 -d \
config=http://10.6.2.124/conf/carhome/%s"% (str(ip),conf)
            print task
            os.system(task)
        print "成功分发！！！"

    except:
        print "异常，等3分钟..."
        time.sleep(180)
        tast_carhome()
if __name__=="__main__":
    tast_carhome()
# -*- coding: utf-8 -*-
#! /usr/bin/env python
import json
import  urllib2
from lxml import etree
item={}
req = urllib2.Request("http://www.w3cschool.cc/python/python-tutorial.html")
html = urllib2.urlopen(req).read()
dom = etree.HTML(html.decode("utf-8"))
titlelist = dom.xpath("//div[@id='leftcolumn']/a/@title")
urllist = dom.xpath("//div[@id='leftcolumn']/a/@href")
for conten in range(urllist.__len__()):
    item['url'] = "http://www.w3cschool.cc/python/"+urllist[conten]
    item['title'] = titlelist[conten]
    print(item["url"])
    print(item["title"])
    i = json.dumps(item)
    with open("dice.txt","a")as w:
        w.write(i + "\n")
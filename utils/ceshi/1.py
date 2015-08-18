# -*- coding: utf-8 -*-
#! /usr/bin/env python
# from mysqlutile import Mysql
import urllib2
from lxml import etree
import re

url = "http://news.baidu.com/ns?word=西安&tn=news&from=news&cl=2&rn=20&ct=1"

html = urllib2.urlopen(url).read()
dom = etree.HTML(html)
lys =[]
d = re.findall(r"\d+",dom.xpath("(//a[@class='c-more_link'])[1]//text()")[0])[0]
# d = dom.xpath("(//a[@class='c-more_link'])[1]//text()")[0]
print d

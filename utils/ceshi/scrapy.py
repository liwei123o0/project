# -*- coding: utf-8 -*-
# ! /usr/bin/env python
import urllib2
from lxml import etree

url ="http://bbs.sxdaily.com.cn/forum.php?mod=viewthread&tid=77518"

req =urllib2.Request(url)
html =urllib2.urlopen(req).read()
dom = etree.HTML(html)
tit = dom.xpath("//span[@class='xi1'][1]/text()")
for i in tit:
    print i

# print html


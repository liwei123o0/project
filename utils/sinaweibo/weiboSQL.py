# -*- coding: utf-8 -*-
# ! /usr/bin/env python
import Login
from Gettext_CH import filter_tags
from mysqlutile import Mysql
from lxml import etree
import urllib2
import sys
import re
reload(sys)
sys.setdefaultencoding("utf-8")

def getHTML(url):
    Login.login()
    html = urllib2.urlopen(url).read()
    return html

if __name__=="__main__":
    html= getHTML("http://weibo.com/cctvcaijing")
    text = filter_tags(html)
    text = text.replace("\\","")
    print text
    with open("sql.txt","w+")as w:
        w.write(text)


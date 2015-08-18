# -*- coding: utf-8 -*-
#! /usr/bin/env python
import urllib2
import re
import time
from mysqlutile import Mysql
def baidushipin():
    keywords =["西安","咸阳","渭南","延安","宝鸡","榆林","铜川","汉中","安康","商洛"]
    for keyword in keywords:
        print keyword
        req =urllib2.Request("http://v.baidu.com/v?word=%s&rn=40&ct=905969664&ie=utf-8&du=0&pd=1&sc=0&pn=0&order=0&db=0&_=1433385366675"% keyword)
        data = urllib2.urlopen(req).read().decode("gbk", errors='ignore')
        data = "".join(data.encode("utf8"))

        ISOTIMEFORMAT ="%Y-%m-%d %X"
        titles = re.findall("ti:.*",data)
        urls   = re.findall("url: \"\/link\?.*",data)
        ly     = re.findall("srcShortUrlExt:.*",data)
        date= time.strftime( ISOTIMEFORMAT, time.localtime() )
        cur =Mysql(host="10.6.2.121")
        cur.conDB()
        groupname="国内视频"
        for i in range(len(titles)):
            urls[i] =re.sub("url: \"","http://v.baidu.com",urls[i])
            urls[i] = re.sub("\.*\"\,","",urls[i])
            ly[i]   = re.sub("srcShortUrlExt: \"","",ly[i])
            ly[i]   = re.sub("\",","",ly[i])
            titles[i]=re.sub("ti:\"","",titles[i])
            titles[i]=re.sub("\",","",titles[i])
            print date,ly[i],titles[i],urls[i],"国内视频"
            if ly[i]=="":
                print "跳过"
                continue
            cur.selDB("INSERT INTO scrapy.news(IR_URLNAME,IR_URLTITLE,IR_CONTENT,IR_SRCNAME,IR_GROUPNAME,IR_SITENAME,IR_URLTIME,IR_CATALOG2) VALUES ('%s','%s','%s','%s','%s','%s','%s','python')"%(urls[i],titles[i],titles[i],ly[i],groupname,ly[i],date))
        cur.closeDB()
if __name__=="__main__":
    baidushipin()

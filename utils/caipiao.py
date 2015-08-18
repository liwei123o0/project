# -*- coding: utf-8 -*-
#! /usr/bin/env python
import urllib2
from  lxml import etree

def caip(url):
    req =urllib2.Request(url)
    html =urllib2.urlopen(req,timeout=30).read()
    dom =etree.HTML(html.decode("utf8"))

    cout =dom.xpath("//tbody[@id='cpdata']/tr")
    cout = len(cout)
    hao =[]
    qiu =[]
    for i in range(1,51):
        if i==50:
            qiui =dom.xpath("//tfoot[@id='now_gross']/tr[1]/td[%s]/text()"%(i+1))
            qiu.append(qiui[0])
            continue
        else:
            haoi =dom.xpath("//tr[@class='thbg01']/th[@width='17'][%s]/text()"%i)
            hao.append(haoi[0].replace("\r\n          ","").replace("\r\n        ",""))
        if i==34:
            continue
        else:
            qiui =dom.xpath("//tfoot[@id='now_gross']/tr[1]/td[%s]/text()"%(i+1))
            qiu.append(qiui[0])
    for i in range(1,len(qiu)+1):
        if i <=33:
            gl=float(qiu[i-1])/float(cout)*100
            print hao[i-1],"-","%s :"%i,gl
        else:
            gl =float(qiu[i-1])/float(cout)*100
            print hao[i-1],"-","%s :"%(i-33),gl
if __name__=="__main__":
    caip("http://zx.caipiao.163.com/trend/ssq_basic.html?beginPeriod=2015001&endPeriod=2015064&historyPeriod=2015065&year=")
    caip("http://zx.caipiao.163.com/trend/ssq_basic.html?beginPeriod=2015001&endPeriod=2015064&historyPeriod=2015065&year=")
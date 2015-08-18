# -*- coding: utf-8 -*-
#! /usr/bin/env python
# -*- coding: utf-8 -*-
#! /usr/bin/env python
import urllib2
from lxml import etree
import re
import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def urlall():
    conn = MySQLdb.connect(host="10.6.2.121",port=3306,user="root",passwd="root",charset="utf8")
    cur = conn.cursor()
    cur.execute("SELECT URL FROM weibo.pcauto_url ORDER BY INSERT_TIME LIMIT 1")
    url = cur.fetchall()[0][0]
    cur.execute("UPDATE weibo.pcauto_url SET COUNTINT = COUNTINT+1 WHERE URL='%s'"%url)
    conn.commit()
    cur.close()
    conn.close()
    return str(url)
def scrapy():
    #从数据库获取URL
    uri = urlall()
    print uri
    html = urllib2.urlopen(uri).read()
    html = html.decode("gbk",errors='ignore')
    dom = etree.HTML(html)
    #提取优惠促销列表
    urls = dom.xpath("//i[@class='iTit']/a/@href")
    conn = MySQLdb.connect(host="10.6.2.121",port=3306,user="root",passwd="root",charset="utf8")
    #详情页提取
    for url in urls:
        cur = conn.cursor()
        req = urllib2.Request(url)
        html = urllib2.urlopen(req).read().decode("gb2312",errors='ignore')
        doc = etree.HTML(html)
        SOURCE_SITE = u"太平洋汽车网"
        EVENT_URL = url
        EVENT_DATETIME = "".join(doc.xpath("//span[@class='crimson']//text() | //div[@class='yhInfo-txt']/p[3]//text()")).encode("utf8",errors='ignore')
        DATE_ISSUE  = "".join(doc.xpath("//p[@class='pfTime']//text() | //div[@class='yhInfo-txt']/p[3]//text() | //p[@class='pfTime']//text()"))
        DEALER_NAME = "".join(doc.xpath("//p[@class='pcom']//text() | //span[@class='dname']/a//text()"))
        EVENT_TOPIC = "".join(doc.xpath("//h1[@class='pTit']//text() | //div[@class='artTitle']//text()"))
        EVENT_TYPE = "".join(doc.xpath("//span[@class='mark']/a[1]//text()"))
        EVENT_DESCR = "".join(doc.xpath("//div[@class='mainTxt']//text() | //div[@class='left660']//text()")).encode("utf8",errors='ignore')
        source_site_id = 5
        #格式化数据
        if EVENT_TYPE == "":
            EVENT_TYPE = u"店铺活动"
        comm = re.compile(r'\d+')
        if comm.search(EVENT_URL):
            dealer_id = comm.search(EVENT_URL).group()

        EVENT_TOPIC = EVENT_TOPIC.replace("\r","").replace("\n","").replace("\t","")
        EVENT_DESCR = EVENT_DESCR.replace("\r","").replace("\t","").replace("\n","")
        DEALER_NAME = DEALER_NAME.replace("\r","").replace("\n","").replace("\t","")
        DESCR = re.compile(r'\/\/javascript.*')
        EVENT_DESCR = DESCR.subn('',EVENT_DESCR)[0]

        if DATE_ISSUE!= "":
            DATE_ISSUE = re.findall(r"[0-9]+年[0-9]+月[0-9]+日|[0-9]+-[0-9]+-[0-9]+",DATE_ISSUE.encode("utf8"))
            DATE_ISSUE = re.sub(r"年|月","-",DATE_ISSUE[0])
            DATE_ISSUE = re.sub(r"日","",DATE_ISSUE)
        else:
            DATE_ISSUE=""
        try:
            print EVENT_URL,EVENT_DATETIME,DATE_ISSUE,DEALER_NAME,EVENT_TOPIC,EVENT_TYPE
            cur.execute("INSERT INTO weibo.EVENT_INFO(SOURCE_SITE,EVENT_URL,EVENT_DATETIME,DATE_ISSUE,DEALER_NAME,EVENT_TOPIC,EVENT_TYPE,EVENT_DESCR,dealer_id,source_site_id) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" %(SOURCE_SITE,EVENT_URL,EVENT_DATETIME,DATE_ISSUE,DEALER_NAME,EVENT_TOPIC,EVENT_TYPE,str(EVENT_DESCR),dealer_id,source_site_id))
        except MySQLdb.Error,e:
                print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        conn.commit()
    conn.close()
while 1:
    scrapy()

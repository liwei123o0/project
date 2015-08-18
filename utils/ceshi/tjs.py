# -*- coding: utf-8 -*-
#! /usr/bin/env python
import urllib2
from lxml import etree
import re
from multiprocessing.dummy import Pool
from mysqlutile import Mysql
import MySQLdb

from  flask import Flask,jsonify
app =Flask(__name__)
@app.route("/q=<url>")
def scrapy(url):
    url =str(url).replace("|!|",'/')
    zs={}
    try:
        req =urllib2.Request(url)
        html =urllib2.urlopen(req,timeout=30).read()
    except:
        conn =MySQLdb.connect(host="10.6.2.121",port=3306,user="root",passwd="root",charset='utf8')
        cur =conn.cursor()
        print u"打开问题：%s"% url
        cur.execute("UPDATE echarts.MEDIA_STAT SET FLAG = 1 WHERE URL='%s'" %url)
        conn.commit()
        cur.close()
        conn.close()
        return ""
    dom =etree.HTML(html)

    if re.findall(r"tieba.baidu.com",url):
        hfs =dom.xpath("(//span[@class='red'])[1]")
        for i in hfs:
            print u"回复数："+i.text
            print u"点击数：",0
            print u"url:%s" % url
            zs['url'] =url
            zs['djs'] =i.text
            zs['hfs'] ='0'
            # zs['name']='百度贴吧'
            return zs
    elif re.findall(r"bbs.ifeng.com",url):
        djs =dom.xpath("//li[@class='ltx3'][2]/span")
        hfs =dom.xpath("//li[@class='ltx3'][3]/span")
        zs['url'] =url
        # zs['name']='凤凰论坛'
        for i in hfs:
            print u"回复数："+i.text
            i =i.text
            zs["hfs"] = i
        for i in djs:
            print u"点击数："+i.text
            i =i.text
            zs["djs"] =i
        print "url:%s" % url
        return zs
    elif re.findall(r"bbs.cnwest.com",url):
        djs =dom.xpath("//span[@class='xi1'][1]/text()")
        hfs =dom.xpath("//span[@class='xi1'][2]/text()")
        zs['url'] =url
        # zs['name']='陕西论坛'
        for i in hfs:
            print u"回复数："+i
            # i =i.text
            zs["hfs"] = i
        for i in djs:
            print u"点击数："+i
            # i =i.text
            zs["djs"] =i
        print "url:%s" % url
        return zs
    elif re.findall(r"deyi.com",url):
        djs =dom.xpath("//div[@class='hm']/text()[2]")
        hfs =dom.xpath("//div[@class='hm']/text()[3]")
        zs['url'] =url
        # zs['name']='得意生活社区'
        for i in hfs:
            print u"回复数："+i
            # i =i.text
            zs["hfs"] = i
        for i in djs:
            print u"点击数："+i
            # i =i.text
            zs["djs"] =i
        print "url:%s" % url
        return zs
    elif re.findall(r"bbs.hsw.cn",url):
        djs =dom.xpath("//span[@class='pages']/a[3]")
        hfs =dom.xpath("//span[@class='pages']/a[4]")
        zs['url'] =url
        # zs['name']='华商论坛'
        for i in hfs:
            i= re.findall(r'[0-9]+',i.text)[0].encode("utf8")
            print u"回复数："+i
            # i =i.text
            zs["hfs"] = i
        for i in djs:
            i= re.findall(r'[0-9]+',i.text)[0].encode("utf8")
            print u"点击数："+i
            # i =i.text
            zs["djs"] =i
        print "url:%s" % url
        return zs
    elif re.findall(r"bbs.ssfeng.com",url):
        djs =dom.xpath("//span[@class='xi1'][1]/text()")
        hfs =dom.xpath("//span[@class='xi1'][2]/text()")
        zs['url'] =url
        # zs['name']='塞上风论坛'
        for i in hfs:
            print u"回复数："+i
            # i =i.text
            zs["hfs"] = i
        for i in djs:
            print u"点击数："+i
            # i =i.text
            zs["djs"] =i
        print "url:%s" % url
        return zs
    elif re.findall(r"bbs.dzwww.com",url):
        djs =dom.xpath("//span[@class='xi1'][1]")
        hfs =dom.xpath("//span[@class='xi1'][2]")
        zs['url'] =url
        # zs['name']='大众论坛'
        for i in hfs:
            print u"回复数："+i.text
            i =i.text
            zs["hfs"] = i
        for i in djs:
            print u"点击数："+i.text
            i =i.text
            zs["djs"] =i
        print "url:%s" % url
        return zs
    elif re.findall(r"163.com",url):
        djs =dom.xpath("(//span[@class='red'])[1]")
        hfs =dom.xpath("(//span[@class='red'])[2]")
        zs['url'] =url
        # zs['name']='网易论坛'
        for i in hfs:
            print u"回复数："+i.text
            # i =i.text
            zs["hfs"] = i.text
        for i in djs:
            print u"点击数："+i.text
            # i =i.text
            zs["djs"] =i.text
        print "url:%s" % url
        return zs
    elif re.findall(r"ltaaa.com",url):
        djs =dom.xpath("//span[@class='xi1'][1]")
        hfs =dom.xpath("//span[@class='xi1'][2]")
        zs['url'] =url
        # zs['name']='龙腾论坛'
        for i in hfs:
            print u"回复数："+i.text
            i =i.text
            zs["hfs"] = i
        for i in djs:
            print u"点击数："+i.text
            i =i.text
            zs["djs"] =i
        print "url:%s" % url
        return zs
    elif re.findall(r"sxdaily.com.cn",url):
        djs =dom.xpath("//span[@class='xi1'][1]")
        hfs =dom.xpath("//span[@class='xi1'][2]")
        zs['url'] =url
        # zs['name']='大秦岭论坛'
        for i in hfs:
            print u"回复数："+i.text
            i =i.text
            zs["hfs"] = i
        for i in djs:
            print u"点击数："+i.text
            i =i.text
            zs["djs"] =i
        print "url:%s" % url
        return zs
    elif re.findall(r"chengshiluntan.com",url):
        djs =dom.xpath("//span[@class='y comiis_cks']/strong")
        hfs =dom.xpath("//span[@class='y comiis_hfs']/strong")
        zs['url'] =url
        # zs['name']='城市论坛'
        for i in hfs:
            print u"回复数："+i.text
            i =i.text
            zs["hfs"] = i
        for i in djs:
            print u"点击数："+i.text
            i =i.text
            zs["djs"] =i
        print "url:%s" % url
        return zs
if __name__=="__main__":
    # app.run(host="0.0.0.0",port=80,debug=True)
    #多线程
    # urls =['http://bbs.baby.163.com/bbs/bbphoto/459909816.html','http://www.chengshiluntan.com/1002239-1.html','http://tieba.baidu.com/p/3851338126']
    # poll =Pool(3)
    # html = poll.map(scrapy,urls)
    # poll.close()
    # poll.join()

    conn =MySQLdb.connect(host="10.6.2.121",port=3306,user="root",passwd="root",charset='utf8')
    cur =conn.cursor()
    cur.execute("SELECT URL FROM echarts.MEDIA_STAT WHERE FLAG=1 OR FLAG=2 LIMIT 13")
    urls = cur.fetchall()
    for url in urls:
        url = url[0]
        zs = scrapy(url)
        try:
            cur.execute("UPDATE echarts.MEDIA_STAT SET FLAG = 1,REPLY_COMMONS='%s',BROWER_CLICKS='%s'  WHERE URL='%s'" %(zs["hfs"],zs["djs"],url))
            conn.commit()
        except:
            print u"未找到或问题url：%s"% url
            cur.execute("UPDATE echarts.MEDIA_STAT SET FLAG = 2 WHERE URL='%s'" %url)
            conn.commit()
            continue
    cur.close()
    conn.close()
    # print scrapy("http://bbs.sxdaily.com.cn/forum.php?mod=viewthread&tid=77518")
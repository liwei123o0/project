# -*- coding: utf-8 -*-
#! /usr/bin/env python
import urllib2
import re
from lxml import etree
import MySQLdb
class scrapy(object):

    def __init__(self):
        self.conn = MySQLdb.connect(host="10.6.2.121",user="root",passwd="root",port=3306,charset="utf8")
        self.cur = self.conn.cursor()

    def loadkeyword(self):
        #批量插入关键词
        # with open("ceshi.txt","rb")as f:
        #     words =f.readlines()
        # for word in words:
        #     self.cur.execute("INSERT INTO weibo.keyword_fenxi(keyword) VALUES ('%s')"%word)

        self.cur.execute("SELECT keyword FROM weibo.keyword_fenxi ORDER BY countint LIMIT 1")
        word =self.cur.fetchall()[0][0].encode("utf8")
        self.cur.execute("UPDATE weibo.keyword_fenxi SET countint = countint+1 WHERE keyword='%s'"%word)
        self.conn.commit()
        return word
    def loadsql(self):
        self.cur.execute("SELECT IR_URLTITLE FROM zjfx.news14 WHERE REPORT_COUNT_STR IS NULL LIMIT 1")
        title = self.cur.fetchall()[0][0].encode("utf8")
        self.cur.execute("UPDATE zjfx.news14 SET REPORT_COUNT_STR = 0 WHERE IR_URLTITLE='%s'"%title)
        self.conn.commit()
        return title
    def craw(self):
        cout =0
        word = self.loadkeyword()
        word1 = urllib2.quote(word)
        uri = 'http://news.baidu.com/ns?from=news&cl=2&pn=0&clk=sortbyrel&bt=1401552000&y0=2014&m0=6&d0=1&y1=2015&m1=6&d1=30&et=1435679999&q1=%s&begin_date=2014-6-1&end_date=2015-6-30&tn=newsdy&ct=1&rn=50'%word1
        html = urllib2.urlopen(uri,timeout=5).read()
        dom = etree.HTML(html)
        if str(dom.xpath("//p[@id='page']/a/text()"))=="[u'\u4e0b\u4e00\u9875>']":
            while 1:
                loop = dom.xpath("//div[@class='result']")
                for i in loop:
                    title = "".join(i.xpath(".//h3/a//text()")).encode("utf8")
                    url   = "".join(i.xpath(".//h3/a/@ href")).encode("utf8")
                    ly   = re.split(r"\w+","".join(i.xpath(".//p[@class='c-author']/text()")))[0].encode("utf8")
                    date = re.findall("\d+年\d+月\d+日\s+\d+:\d+","".join(i.xpath(".//p[@class='c-author']/text()")).encode("utf8"))[0]
                    conten =  "".join(i.xpath(".//div[@class='c-summary c-row ']//text()")).encode("utf8")
                    url2 =''

                    if i.xpath(".//a[@class='c-more_link']/@href"):
                        lys =[]
                        uri2 ="http://news.baidu.com"+"".join(i.xpath(".//a[@class='c-more_link']/@href"))
                        html2 = urllib2.urlopen(uri2,timeout=5).read()
                        dom2 = etree.HTML(html2)
                        ly2 = dom2.xpath("//div[@class='result']//p[@class='c-author']/text()")
                        for i2 in ly2:
                            i2 = "".join(re.split(r"\xa0\xa0",i2)[0])
                            lys.append(i2)
                        ly2 = ",".join(lys).encode("utf8")
                        ly = ly2
                        url2 =uri2
                        print uri2,ly
                    try:
                        self.cur.execute("INSERT INTO zjfx.news14(IR_URLNAME,IR_URLTITLE,IR_CONTENT,IR_SRCNAME,IR_URLTIME,IR_KEYWORD) VALUES ('%s','%s','%s','%s','%s','%s')"%(url,title,conten,ly,date,word))
                        self.conn.commit()
                        if url2:
                            self.cur.execute("UPDATE zjfx.news14 SET IR_SRCNAME = '%s',IR_URLNAME2='%s' WHERE IR_URLNAME='%s'"%(ly,url2,url))
                            self.conn.commit()
                    except MySQLdb.Error,e:
                        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
                cout+=50
                urii =uri.replace(u'pn=0',u'pn=%s'%cout)
                urii = urii.encode("utf8")
                # print "下一页：%s"%urii
                html = urllib2.urlopen(urii,timeout=5).read()
                dom = etree.HTML(html)
                loop = dom.xpath("//div[@class='result']")
                for i in loop:
                    title = "".join(i.xpath(".//h3/a//text()")).encode("utf8")
                    url   = "".join(i.xpath(".//h3/a/@ href")).encode("utf8")
                    ly   = re.split(r"\w+","".join(i.xpath(".//p[@class='c-author']/text()")))[0].encode("utf8")
                    date = re.findall("\d+年\d+月\d+日\s+\d+:\d+","".join(i.xpath(".//p[@class='c-author']/text()")).encode("utf8"))[0]
                    conten =  "".join(i.xpath(".//div[@class='c-summary c-row ']//text()")).encode("utf8")
                    url2 =''
                    if i.xpath(".//a[@class='c-more_link']/@href"):
                        lys =[]
                        uri2 ="http://news.baidu.com"+"".join(i.xpath(".//a[@class='c-more_link']/@href"))
                        html2 = urllib2.urlopen(uri2,timeout=5).read()
                        dom2 = etree.HTML(html2)
                        ly2 = dom2.xpath("//div[@class='result']//p[@class='c-author']/text()")
                        for i2 in ly2:
                            i2 = "".join(re.split(r"\xa0\xa0",i2)[0])
                            lys.append(i2)
                        ly2 = ",".join(lys).encode("utf8")
                        ly = ly2
                        url2 =uri2
                        print uri2,ly
                    try:
                        self.cur.execute("INSERT INTO zjfx.news14(IR_URLNAME,IR_URLTITLE,IR_CONTENT,IR_SRCNAME,IR_URLTIME,IR_KEYWORD) VALUES ('%s','%s','%s','%s','%s','%s')"%(url,title,conten,ly,date,word))
                        self.conn.commit()
                        if url2:
                            self.cur.execute("UPDATE zjfx.news14 SET IR_SRCNAME = '%s',IR_URLNAME2='%s' WHERE IR_URLNAME='%s'"%(ly,url2,url))
                            self.conn.commit()
                    except MySQLdb.Error,e:
                        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
                break
        else:
            loop = dom.xpath("//div[@class='result']")
            for i in loop:
                title = "".join(i.xpath(".//h3/a//text()")).encode("utf8")
                url   = "".join(i.xpath(".//h3/a/@ href")).encode("utf8")
                ly   = re.split(r"\w+","".join(i.xpath(".//p[@class='c-author']/text()")))[0].encode("utf8")
                date = re.findall("\d+年\d+月\d+日\s+\d+:\d+","".join(i.xpath(".//p[@class='c-author']/text()")).encode("utf8"))[0]
                conten =  "".join(i.xpath(".//div[@class='c-summary c-row ']//text()")).encode("utf8")

                url2 =''
                if i.xpath(".//a[@class='c-more_link']/@href"):
                    lys =[]
                    uri2 ="http://news.baidu.com"+"".join(i.xpath(".//a[@class='c-more_link']/@href"))
                    html2 = urllib2.urlopen(uri2,timeout=5).read()
                    dom2 = etree.HTML(html2)
                    ly2 = dom2.xpath("//div[@class='result']//p[@class='c-author']/text()")
                    for i2 in ly2:
                        i2 = "".join(re.split(r"\xa0\xa0",i2)[0])
                        lys.append(i2)
                    ly2 = ",".join(lys).encode("utf8")
                    ly = ly2
                    url2 =uri2
                    print uri2,ly
                try:
                    self.cur.execute("INSERT INTO zjfx.news14(IR_URLNAME,IR_URLTITLE,IR_CONTENT,IR_SRCNAME,IR_URLTIME,IR_KEYWORD) VALUES ('%s','%s','%s','%s','%s','%s')"%(url,title,conten,ly,date,word))
                    self.conn.commit()
                    if url2:
                        self.cur.execute("UPDATE zjfx.news14 SET IR_SRCNAME = '%s',IR_URLNAME2='%s' WHERE IR_URLNAME='%s'"%(ly,url2,url))
                        self.conn.commit()
                except MySQLdb.Error,e:
                    print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        self.cur.close()
        self.conn.close()
    def crwatitle(self):
        url2 =''
        title = self.loadsql()
        title1 = urllib2.quote("%s"%title)
        uri = 'http://news.baidu.com/ns?word=%s&tn=news&from=news&cl=2&rn=20&ct=1'%title1
        html  = urllib2.urlopen(uri,timeout=5).read()
        dom   = etree.HTML(html)
        if dom.xpath("(//div[@class='result']//a[@class='c-more_link'])[1]/@href"):
            lys =[]
            REPORT_COUNT = re.findall(r"\d+",dom.xpath("(//a[@class='c-more_link'])[1]//text()")[0])[0].encode("utf8")
            uri2 ="http://news.baidu.com"+"".join(dom.xpath("(//div[@class='result']//a[@class='c-more_link'])[1]/@href"))
            html2 = urllib2.urlopen(uri2,timeout=5).read()
            dom2 = etree.HTML(html2)
            ly2 = dom2.xpath("//div[@class='result']//p[@class='c-author']/text()")
            for i2 in ly2:
                i2 = "".join(re.split(r"\xa0\xa0",i2)[0])
                lys.append(i2)
                ly2 = ",".join(lys).encode("utf8")
                url2 =uri2
            print title,url2,ly2,REPORT_COUNT
            try:
                self.cur.execute('UPDATE zjfx.news14 SET IR_URLNAME2="%s",IR_SRCNAME="%s",REPORT_COUNT="%s" WHERE IR_URLTITLE="%s" AND REPORT_COUNT=1'%(url2,ly2,REPORT_COUNT,title))
                self.conn.commit()
            except MySQLdb.Error,e:
                print "Mysql Error %d: %s" % (e.args[0], e.args[1])

        self.cur.close()
        self.conn.close()
while 1:
    try:
        a   = scrapy()
        a.crwatitle()
    except:
        continue
# a   = scrapy()
# a.crwatitle()
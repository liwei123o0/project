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

    def crawl(self):
        cout =0
        word = self.loadkeyword()
        word = urllib2.quote(word)
        uri = 'http://news.baidu.com/ns?from=news&cl=2&pn=0&clk=sortbyrel&bt=1338480000&y0=2012&m0=6&d0=1&y1=2015&m1=6&d1=30&et=1435679999&q1=%s&begin_date=2012-6-1&end_date=2015-6-30&tn=newsdy&ct1=0&ct=0&rn=50&q6='%word
        html = urllib2.urlopen(uri).read()
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
                    try:
                        self.cur.execute("INSERT INTO zjfx.news(IR_URLNAME,IR_URLTITLE,IR_CONTENT,IR_SRCNAME,IR_URLTIME) VALUES ('%s','%s','%s','%s','%s')"%(url,title,conten,ly,date))
                        self.conn.commit()
                    except MySQLdb.Error,e:
                        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
                cout+=50
                urii =uri.replace(u'pn=0',u'pn=%s'%cout)
                urii = urii.encode("utf8")
                # print "下一页：%s"%urii
                html = urllib2.urlopen(urii).read()
                dom = etree.HTML(html)
                loop = dom.xpath("//div[@class='result']")
                for i in loop:
                    title = "".join(i.xpath(".//h3/a//text()")).encode("utf8")
                    url   = "".join(i.xpath(".//h3/a/@ href")).encode("utf8")
                    ly   = re.split(r"\w+","".join(i.xpath(".//p[@class='c-author']/text()")))[0].encode("utf8")
                    date = re.findall("\d+年\d+月\d+日\s+\d+:\d+","".join(i.xpath(".//p[@class='c-author']/text()")).encode("utf8"))[0]
                    conten =  "".join(i.xpath(".//div[@class='c-summary c-row ']//text()")).encode("utf8")
                    try:
                        self.cur.execute("INSERT INTO zjfx.news(IR_URLNAME,IR_URLTITLE,IR_CONTENT,IR_SRCNAME,IR_URLTIME) VALUES ('%s','%s','%s','%s','%s')"%(url,title,conten,ly,date))
                        self.conn.commit()
                    except MySQLdb.Error,e:
                        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
                if str(dom.xpath("//p[@id='page']/a/text()"))=="[u'<\u4e0a\u4e00\u9875']":
                    # print "共%s页:"%(cout/50+1)
                    break
        else:
            loop = dom.xpath("//div[@class='result']")
            for i in loop:
                title = "".join(i.xpath(".//h3/a//text()")).encode("utf8")
                url   = "".join(i.xpath(".//h3/a/@ href")).encode("utf8")
                ly   = re.split(r"\w+","".join(i.xpath(".//p[@class='c-author']/text()")))[0].encode("utf8")
                date = re.findall("\d+年\d+月\d+日\s+\d+:\d+","".join(i.xpath(".//p[@class='c-author']/text()")).encode("utf8"))[0]
                conten =  "".join(i.xpath(".//div[@class='c-summary c-row ']//text()")).encode("utf8")
                try:
                    self.cur.execute("INSERT INTO zjfx.news(IR_URLNAME,IR_URLTITLE,IR_CONTENT,IR_SRCNAME,IR_URLTIME) VALUES ('%s','%s','%s','%s','%s')"%(url,title,conten,ly,date))
                    self.conn.commit()
                except MySQLdb.Error,e:
                    print "Mysql Error %d: %s" % (e.args[0], e.args[1])
                # print "else:%s"%uri
            # print "else:%s"%uri
        self.cur.close()
        self.conn.close()
    def crawl2(self):
        cout =0
        word = self.loadkeyword()
        word1 = urllib2.quote(word)
        uri = 'http://news.baidu.com/ns?from=news&cl=2&pn=0&clk=sortbyrel&bt=1338480000&y0=2012&m0=6&d0=1&y1=2013&m1=6&d1=30&et=1435679999&q1=%s&begin_date=2012-6-1&end_date=2013-6-30&tn=newsdy&ct=1&rn=50&q6='%word1
        html = urllib2.urlopen(uri).read()
        dom = etree.HTML(html)
        if str(dom.xpath("//p[@id='page']/a/text()"))=="[u'\u4e0b\u4e00\u9875>']":
            while 1:
                loop = dom.xpath("//div[@class='result']")
                for i in loop:
                    ly3=''
                    if i.xpath(".//a[@class='c-more_link']/@href"):
                        lys =[]
                        print "ok"
                        uri2 ="http://news.baidu.com"+"".join(i.xpath(".//a[@class='c-more_link']/@href"))
                        html2 = urllib2.urlopen(uri2).read()
                        dom2 = etree.HTML(html2)
                        # title2 = "".join(dom2.xpath("(//div[@class='result']//h3//a)[last()]//text()")).encode("utf8")
                        # url2   = "".join(i.xpath("(//div[@class='result']//h3//a)[last()]/@ href")).encode("utf8")
                        # date2 = re.findall("\d+年\d+月\d+日\s+\d+:\d+","".join(dom2.xpath("(//div[@class='result']//p[@class='c-author'])[last()]/text()")).encode("utf8"))[0]
                        # conten2 =  "".join(dom2.xpath("(//div[@class='result']//div[@class='c-summary c-row '])[last()]//text()")).encode("utf8")
                        ly2 = dom2.xpath("//div[@class='result']//p[@class='c-author']/text()")
                        for i2 in ly2:
                            i2 = "".join(re.split(r"\xa0\xa0",i2)[0])
                            lys.append(i2)
                        ly2 = ",".join(lys).encode("utf8")
                        ly3 =ly2
                        print uri2,ly2
                        try:
                            # self.cur.execute("INSERT INTO zjfx.news12(IR_URLNAME,IR_URLTITLE,IR_CONTENT,IR_SRCNAME,IR_URLTIME,IR_KEYWORD,IR_URLNAME2) VALUES ('%s','%s','%s','%s','%s','%s','%s')"%(url2,title2,conten2,ly2,date2,word,uri2))
                            self.cur.execute("INSERT INTO zjfx.news12(IR_URLNAME2) VALUES ('%s')"%(uri2))
                            self.conn.commit()
                        except MySQLdb.Error,e:
                            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
                    title = "".join(i.xpath(".//h3/a//text()")).encode("utf8")
                    url   = "".join(i.xpath(".//h3/a/@ href")).encode("utf8")
                    ly   = re.split(r"\w+","".join(i.xpath(".//p[@class='c-author']/text()")))[0].encode("utf8")
                    date = re.findall("\d+年\d+月\d+日\s+\d+:\d+","".join(i.xpath(".//p[@class='c-author']/text()")).encode("utf8"))[0]
                    conten =  "".join(i.xpath(".//div[@class='c-summary c-row ']//text()")).encode("utf8")
                    try:
                        self.cur.execute("INSERT INTO zjfx.news12(IR_URLNAME,IR_URLTITLE,IR_CONTENT,IR_SRCNAME,IR_URLTIME,IR_KEYWORD) VALUES ('%s','%s','%s','%s','%s','%s')"%(url,title,conten,ly,date,word))
                        if ly3:
                            self.cur.execute("UPDATE zjfx.news12 SET IR_SRCNAME = %s WHERE IR_URLNAME='%s'"%(ly3,url))
                        self.conn.commit()
                    except MySQLdb.Error,e:
                        print "Mysql Error %d: %s" % (e.args[0], e.args[1])

                    # else:
                    #     title = "".join(i.xpath(".//h3/a//text()")).encode("utf8")
                    #     url   = "".join(i.xpath(".//h3/a/@ href")).encode("utf8")
                    #     ly   = re.split(r"\w+","".join(i.xpath(".//p[@class='c-author']/text()")))[0].encode("utf8")
                    #     date = re.findall("\d+年\d+月\d+日\s+\d+:\d+","".join(i.xpath(".//p[@class='c-author']/text()")).encode("utf8"))[0]
                    #     conten =  "".join(i.xpath(".//div[@class='c-summary c-row ']//text()")).encode("utf8")
                    #     try:
                    #         self.cur.execute("INSERT INTO zjfx.news12(IR_URLNAME,IR_URLTITLE,IR_CONTENT,IR_SRCNAME,IR_URLTIME,IR_KEYWORD) VALUES ('%s','%s','%s','%s','%s','%s')"%(url,title,conten,ly,date,word))
                    #         self.conn.commit()
                    #     except MySQLdb.Error,e:
                    #         print "Mysql Error %d: %s" % (e.args[0], e.args[1])

                    # title = "".join(i.xpath(".//h3/a//text()")).encode("utf8")
                    # url   = "".join(i.xpath(".//h3/a/@ href")).encode("utf8")
                    # ly   = re.split(r"\w+","".join(i.xpath(".//p[@class='c-author']/text()")))[0].encode("utf8")
                    # date = re.findall("\d+年\d+月\d+日\s+\d+:\d+","".join(i.xpath(".//p[@class='c-author']/text()")).encode("utf8"))[0]
                    # conten =  "".join(i.xpath(".//div[@class='c-summary c-row ']//text()")).encode("utf8")
                    # try:
                    #     self.cur.execute("INSERT INTO zjfx.news12(IR_URLNAME,IR_URLTITLE,IR_CONTENT,IR_SRCNAME,IR_URLTIME,IR_KEYWORD) VALUES ('%s','%s','%s','%s','%s','%s')"%(url,title,conten,ly,date,word))
                    #     self.conn.commit()
                    # except MySQLdb.Error,e:
                    #     print "Mysql Error %d: %s" % (e.args[0], e.args[1])
                cout+=50
                urii =uri.replace(u'pn=0',u'pn=%s'%cout)
                urii = urii.encode("utf8")
                # print "下一页：%s"%urii
                html = urllib2.urlopen(urii).read()
                dom = etree.HTML(html)
                loop = dom.xpath("//div[@class='result']")
                for i in loop:
                    ly3=''
                    # title = "".join(i.xpath(".//h3/a//text()")).encode("utf8")
                    # url   = "".join(i.xpath(".//h3/a/@ href")).encode("utf8")
                    # ly   = re.split(r"\w+","".join(i.xpath(".//p[@class='c-author']/text()")))[0].encode("utf8")
                    # date = re.findall("\d+年\d+月\d+日\s+\d+:\d+","".join(i.xpath(".//p[@class='c-author']/text()")).encode("utf8"))[0]
                    # conten =  "".join(i.xpath(".//div[@class='c-summary c-row ']//text()")).encode("utf8")
                    # try:
                    #     self.cur.execute("INSERT INTO zjfx.news12(IR_URLNAME,IR_URLTITLE,IR_CONTENT,IR_SRCNAME,IR_URLTIME,IR_KEYWORD) VALUES ('%s','%s','%s','%s','%s','%s')"%(url,title,conten,ly,date,word))
                    #     self.conn.commit()
                    # except MySQLdb.Error,e:
                    #     print "Mysql Error %d: %s" % (e.args[0], e.args[1])
                    if i.xpath(".//a[@class='c-more_link']/@href"):
                        lys =[]
                        print "ok"
                        uri2 ="http://news.baidu.com"+"".join(i.xpath(".//a[@class='c-more_link']/@href"))
                        html2 = urllib2.urlopen(uri2).read()
                        dom2 = etree.HTML(html2)
                        # title2 = "".join(dom2.xpath("(//div[@class='result']//h3//a)[last()]//text()")).encode("utf8")
                        # url2   = "".join(i.xpath("(//div[@class='result']//h3//a)[last()]/@ href")).encode("utf8")
                        # date2 = re.findall("\d+年\d+月\d+日\s+\d+:\d+","".join(dom2.xpath("(//div[@class='result']//p[@class='c-author'])[last()]/text()")).encode("utf8"))[0]
                        # conten2 =  "".join(dom2.xpath("(//div[@class='result']//div[@class='c-summary c-row '])[last()]//text()")).encode("utf8")
                        ly2 = dom2.xpath("//div[@class='result']//p[@class='c-author']/text()")
                        for i2 in ly2:
                            i2 = "".join(re.split(r"\xa0\xa0",i2)[0])
                            lys.append(i2)
                        ly2 = ",".join(lys).encode("utf8")
                        ly3=ly2
                        print uri2,ly2
                        try:
                            # self.cur.execute("INSERT INTO zjfx.news12(IR_URLNAME,IR_URLTITLE,IR_CONTENT,IR_SRCNAME,IR_URLTIME,IR_KEYWORD,IR_URLNAME2) VALUES ('%s','%s','%s','%s','%s','%s','%s')"%(url2,title2,conten2,ly2,date2,word,uri2))
                            self.cur.execute("INSERT INTO zjfx.news12(IR_URLNAME2) VALUES ('%s')"%(uri2))
                            self.conn.commit()
                        except MySQLdb.Error,e:
                            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
                    title = "".join(i.xpath(".//h3/a//text()")).encode("utf8")
                    url   = "".join(i.xpath(".//h3/a/@ href")).encode("utf8")
                    ly   = re.split(r"\w+","".join(i.xpath(".//p[@class='c-author']/text()")))[0].encode("utf8")
                    date = re.findall("\d+年\d+月\d+日\s+\d+:\d+","".join(i.xpath(".//p[@class='c-author']/text()")).encode("utf8"))[0]
                    conten =  "".join(i.xpath(".//div[@class='c-summary c-row ']//text()")).encode("utf8")
                    try:
                        self.cur.execute("INSERT INTO zjfx.news12(IR_URLNAME,IR_URLTITLE,IR_CONTENT,IR_SRCNAME,IR_URLTIME,IR_KEYWORD) VALUES ('%s','%s','%s','%s','%s','%s')"%(url,title,conten,ly,date,word))
                        if ly3:
                            self.cur.execute("UPDATE zjfx.news12 SET IR_SRCNAME = %s WHERE IR_URLNAME='%s'"%(ly3,url))
                        self.conn.commit()
                    except MySQLdb.Error,e:
                        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
                    # else:
                    #     title = "".join(i.xpath(".//h3/a//text()")).encode("utf8")
                    #     url   = "".join(i.xpath(".//h3/a/@ href")).encode("utf8")
                    #     ly   = re.split(r"\w+","".join(i.xpath(".//p[@class='c-author']/text()")))[0].encode("utf8")
                    #     date = re.findall("\d+年\d+月\d+日\s+\d+:\d+","".join(i.xpath(".//p[@class='c-author']/text()")).encode("utf8"))[0]
                    #     conten =  "".join(i.xpath(".//div[@class='c-summary c-row ']//text()")).encode("utf8")
                    #     try:
                    #         self.cur.execute("INSERT INTO zjfx.news12(IR_URLNAME,IR_URLTITLE,IR_CONTENT,IR_SRCNAME,IR_URLTIME,IR_KEYWORD) VALUES ('%s','%s','%s','%s','%s','%s')"%(url,title,conten,ly,date,word))
                    #         self.conn.commit()
                    #     except MySQLdb.Error,e:
                    #         print "Mysql Error %d: %s" % (e.args[0], e.args[1])
                break
        # else:
        #     loop = dom.xpath("//div[@class='result']")
        #     for i in loop:
        #         if i.xpath(".//a[@class='c-more_link']/@href"):
        #             lys =[]
        #             print "ok"
        #             uri2 ="http://news.baidu.com"+"".join(i.xpath(".//a[@class='c-more_link']/@href"))
        #             html2 = urllib2.urlopen(uri2).read()
        #             dom2 = etree.HTML(html2)
        #             title2 = "".join(dom2.xpath("(//div[@class='result']//h3//a)[1]//text()")).encode("utf8")
        #             url2   = "".join(i.xpath("(//div[@class='result']//h3//a)[1]/@ href")).encode("utf8")
        #             date2 = re.findall("\d+年\d+月\d+日\s+\d+:\d+","".join(i.xpath("(//div[@class='result']//p[@class='c-author'])[1]/text()")).encode("utf8"))[0]
        #             conten2 =  "".join(i.xpath("(//div[@class='result']//div[@class='c-summary c-row '])[1]//text()")).encode("utf8")
        #             ly2 = dom.xpath("//div[@class='result']//p[@class='c-author']/text()")
        #             for i2 in ly2:
        #                 i2 = "".join(re.split(r"\xa0\xa0",i2)[0])
        #                 lys.append(i2)
        #             ly2 = ",".join(lys).encode("utf8")
        #             try :
        #                 self.cur.execute("INSERT INTO zjfx.news12(IR_URLNAME,IR_URLTITLE,IR_CONTENT,IR_SRCNAME,IR_URLTIME,IR_KEYWORD,IR_URLNAME2) VALUES ('%s','%s','%s','%s','%s','%s','%s')"%(url2,title2,conten2,ly2,date2,word,url2))
        #                 self.conn.commit()
        #             except MySQLdb.Error,e:
        #                 print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        else:
            loop = dom.xpath("//div[@class='result']")
            for i in loop:
                ly3=''
                if i.xpath(".//a[@class='c-more_link']/@href"):
                    lys =[]
                    print "ok"
                    uri2 ="http://news.baidu.com"+"".join(i.xpath(".//a[@class='c-more_link']/@href"))
                    html2 = urllib2.urlopen(uri2).read()
                    dom2 = etree.HTML(html2)
                    # title2 = "".join(dom2.xpath("(//div[@class='result']//h3//a)[last()]//text()")).encode("utf8")
                    # url2   = "".join(i.xpath("(//div[@class='result']//h3//a)[last()]/@ href")).encode("utf8")
                    # date2 = re.findall("\d+年\d+月\d+日\s+\d+:\d+","".join(dom2.xpath("(//div[@class='result']//p[@class='c-author'])[last()]/text()")).encode("utf8"))[0]
                    # conten2 =  "".join(dom2.xpath("(//div[@class='result']//div[@class='c-summary c-row '])[last()]//text()")).encode("utf8")
                    ly2 = dom2.xpath("//div[@class='result']//p[@class='c-author']/text()")
                    for i2 in ly2:
                        i2 = "".join(re.split(r"\xa0\xa0",i2)[0])
                        lys.append(i2)
                    ly2 = ",".join(lys).encode("utf8")
                    ly3=ly2
                    print uri2,ly2
                    try:
                        # self.cur.execute("INSERT INTO zjfx.news12(IR_URLNAME,IR_URLTITLE,IR_CONTENT,IR_SRCNAME,IR_URLTIME,IR_KEYWORD,IR_URLNAME2) VALUES ('%s','%s','%s','%s','%s','%s','%s')"%(url2,title2,conten2,ly2,date2,word,uri2))
                        self.cur.execute("INSERT INTO zjfx.news12(IR_URLNAME2) VALUES ('%s')"%(uri2))
                        self.conn.commit()
                    except MySQLdb.Error,e:
                        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
                title = "".join(i.xpath(".//h3/a//text()")).encode("utf8")
                url   = "".join(i.xpath(".//h3/a/@ href")).encode("utf8")
                ly   = re.split(r"\w+","".join(i.xpath(".//p[@class='c-author']/text()")))[0].encode("utf8")
                date = re.findall("\d+年\d+月\d+日\s+\d+:\d+","".join(i.xpath(".//p[@class='c-author']/text()")).encode("utf8"))[0]
                conten =  "".join(i.xpath(".//div[@class='c-summary c-row ']//text()")).encode("utf8")
                try:
                    self.cur.execute("INSERT INTO zjfx.news12(IR_URLNAME,IR_URLTITLE,IR_CONTENT,IR_SRCNAME,IR_URLTIME,IR_KEYWORD) VALUES ('%s','%s','%s','%s','%s','%s')"%(url,title,conten,ly,date,word))
                    if ly3:
                        self.cur.execute("UPDATE zjfx.news12 SET IR_SRCNAME = %s WHERE IR_URLNAME='%s'"%(ly3,url))
                    self.conn.commit()
                except MySQLdb.Error,e:
                    print "Mysql Error %d: %s" % (e.args[0], e.args[1])
                # else:
                #     title = "".join(i.xpath(".//h3/a//text()")).encode("utf8")
                #     url   = "".join(i.xpath(".//h3/a/@ href")).encode("utf8")
                #     ly   = re.split(r"\w+","".join(i.xpath(".//p[@class='c-author']/text()")))[0].encode("utf8")
                #     date = re.findall("\d+年\d+月\d+日\s+\d+:\d+","".join(i.xpath(".//p[@class='c-author']/text()")).encode("utf8"))[0]
                #     conten =  "".join(i.xpath(".//div[@class='c-summary c-row ']//text()")).encode("utf8")
                #     try:
                #         self.cur.execute("INSERT INTO zjfx.news12(IR_URLNAME,IR_URLTITLE,IR_CONTENT,IR_SRCNAME,IR_URLTIME,IR_KEYWORD) VALUES ('%s','%s','%s','%s','%s','%s')"%(url,title,conten,ly,date,word))
                #         self.conn.commit()
                #     except MySQLdb.Error,e:
                #         print "Mysql Error %d: %s" % (e.args[0], e.args[1])
                # print "else:%s"%uri
            # print "else:%s"%uri
        self.cur.close()
        self.conn.close()
while 1:
    a = scrapy()
    a.crawl2()
    # a.loadkeyword()
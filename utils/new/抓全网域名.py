# -*- coding: utf-8 -*-
#! /usr/bin/env python
import urllib2
import MySQLdb
import re
import time
conn= MySQLdb.connect(
	        host='127.0.0.1',
	        port = 3306,
	        user='root',
	        passwd='root',
	        db ='',
	        )
cur = conn.cursor()
#爬取全网域名入库
class Spider_Web(object):
    #获取url
    def getUrl(self,urls):
        if urls == '':
            urls = "http://www.yilongnews.com"
        try:
            status=urllib2.urlopen(urls,timeout=15).code
        except:
            print urls
            time.sleep(5)
            status = 203
        if status == 200:
            html = Spider_Web().getHtml(urls)
            cc = Spider_Web().getImg(html)
            cc = list(set(cc))
            for aa in cc:
                Spider_Web().isFind(aa)
        else:
            sql2 = u"update test.get_url set is_geted = '2' where url = '%s'" % (urls)
            cur.execute(sql2)
            time.sleep(0.02)
            conn.commit()
        return Spider_Web().findMin()
    #数据库中查找最小的 没有爬行过的id ，再次爬行
    def findMin(self):
        sql = u"select min(id) from test.get_url where is_geted = 0"
        cur.execute(sql)
        res1 = cur.fetchall()
        urld = res1[0][0]
        print urld
        sql1 = u"select url from test.get_url where id = '%d'" % (urld)
        cur.execute(sql1)
        cds=cur.fetchall()
        again = cds[0][0]
        sql2 = u"update test.get_url set is_geted = '1' where id = '%d'" % (urld)
        cur.execute(sql2)
        conn.commit()
        print again
        return	Spider_Web().getUrl(again)
    #获取网页内容
    def getHtml(self,url):
        try:
            page = urllib2.urlopen(url,timeout=15)
        except:
            url="http://www.qq.com"
            page =urllib2.urlopen(url,timeout=15)
        html = page.read()
        return html
    #正则表达式，获取url
    def getImg(self,html):
        reg = r'[a-zA-z]+:\/\/www?\.[0-9a-zA-z_]+[\.a-z]+'
        imgre = re.compile(reg)
        imglist = re.findall(imgre,html)
        return imglist
    # 写入数据库
    def isFind(self,aa):
        print aa
        statement = u"select * from test.get_url where url = '%s'" % (aa)
        result = cur.execute(statement)
        conn.commit()
        if result == 0:
            x = u"INSERT INTO test.get_url set url = '%s'" % (aa)
            cur.execute(x)
        return
if __name__=="__main__":
    urls = "http://www.yilongnews.com"
    try:
        starts = Spider_Web()
        starts.getUrl(urls)
        cur.close()
        conn.close()
    except:
        starts = Spider_Web()
        starts.getUrl(urls)
        cur.close()
        conn.close()
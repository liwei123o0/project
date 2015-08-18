# -*- coding: utf-8 -*-
#! /usr/bin/env python
'''
import MySQLdb
import threading
import urllib2
import re
import time

conn= MySQLdb.connect(
    host='localhost',
    port = 3306,
    user='root',
    passwd='root',
    db ='',
    )
cur = conn.cursor()

class newGet(object):
    def __init__(self,url):
        self.url= url

    def findMin(self):
        #存入数据库以后，从数据库里面从id最小的开始获取，写入数据库。
        print "isfind"
        sql = u"select url from test.get_url  where is_geted = 0 order by id desc limit 10"
        cur.execute(sql)
        res1 = cur.fetchall()
        #for i in range(10):
             #res1[i][0]
        return res1

    #获取网页内容
    def getHtml(self,url):

        try:
            page = urllib2.urlopen(url,timeout=15)
        except:
            url = "http://www.yilongnews.com"
            page = urllib2.urlopen(url)
        print url
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
       # print aa
        statement = u"select * from test.get_url where url = '%s'" % (aa)
        result = cur.execute(statement)
        conn.commit()
        if result == 0:
            x = u"INSERT INTO test.get_url set url = '%s'" % (aa)
            mm = cur.execute(x)
        print "Yes ! geted"
        return
    def run(self,i):
        while 1:
            urls = n.findMin()
            url=  urls[i][0]
            geth = n.getHtml(url)
            geti = n.getImg(geth)
            geti = list(set(geti))
            for aa in geti:
                print aa
            self.isFind(aa)
            time.sleep(0.02)
if __name__ == '__main__':
    n = newGet("http://www.yilongnews.com")
    for i in xrange(10):
        t =threading.Thread(target=n.run(i))
        t.setDaemon(True)
        t.start()
        t.join()
'''
##队列
# -*- coding: utf-8 -*-
#! /usr/bin/env python
import MySQLdb
import threading
import urllib2
import re
import time
import Queue
queue = Queue.Queue()

conn= MySQLdb.connect(
    host='localhost',
    port = 3306,
    user='root',
    passwd='root',
    db ='',
    )
cur = conn.cursor()

class newGet(object):
    def __init__(self,url):
        self.url= url

    def findMin(self):
        #存入数据库以后，从数据库里面从id最小的开始获取，写入数据库。
        print "isfind"
        cur = conn.cursor()
        sql = u"select url from test.get_url  where is_geted = 0 order by id asc limit 20"
        cur.execute(sql)
        res1 = cur.fetchall()

        # #print res1
        for rn in res1:
            urld = rn[0]
            print urld
            #把状态改成 1
            sql2 = u"update test.get_url set is_geted = '1' where url = '%s'" % (urld)
            cur.execute(sql2)
            conn.commit()
        #cur.close()
        # cur = conn.cursor()
        return res1

    #获取网页内容
    def getHtml(self,url):
        if url == '':
            url = "http://www.php100.com"
        try:
            status=urllib2.urlopen(url,timeout=15).code
        except:
            print url
            status=urllib2.urlopen(url,timeout=15).code    #打不开获取不到 状态吗
            print status
        if status == 200:
            try:
                page = urllib2.urlopen(url,timeout=15)
            except:
                 url = "http://www.php100.com"
                # page = r"\<a href=\"http://www.php100.com\"> <\/a>"
                 print "111111111111111"
            print url
            html = page.read()                # 这里的错误，
        else:
            print url
            print "2222222222222222222222222222222222222222222222222222222222222222"
            try:
                sql2 = u"update test.get_url set is_geted = '2' where url = '%s'" % (url)
                cur.execute(sql2)
                conn.commit()
                cur.close()
                time.sleep(0.02)
                html = "12321321"                 # 这里的错误，
            except:
                html = "12321321"
        print status
       # print html
        return html

#正则表达式，获取url
    def getImg(self,html):
        reg = r'[a-zA-z]+:\/\/www?\.[0-9a-zA-z_]+[\.a-z]+'
        imgre = re.compile(reg)
        imglist = re.findall(imgre,html)
        return imglist
    # 写入数据库
    def isFind(self,aa):
        try:
            sql = u"select * from test.get_url where url = '%s'" %(aa)
            result = cur.execute(sql)
            conn.commit()

           # print resul
            if result == 0:
                x = u"INSERT INTO test.get_url set url = '%s'" %(aa)
                mm = cur.execute(x)
                print "写入成功，网站 %s" % (aa)
            else:
                pass
        except:
            time.sleep(0.2)
        return
    def run(self,i):
        url= i
      #  print url
        geth = n.getHtml(url)
       # print '1'
        geti = n.getImg(geth)
        cc = list(set(geti))
        for aa in cc:
            queue.put(aa)
            #self.isFind(aa)
        return
if __name__ == '__main__':

    while 1:
        cur = conn.cursor()
        n = newGet("http://www.php100.com")
        try:
            list1 = n.findMin()
            cur.close()
            cur = conn.cursor()
            #print list
            threads = []
            files = range(len(list1))
            #创建线程
            for i in files:
                t = threading.Thread(target=n.run,args=(list1[i][0],))
                threads.append(t)
            for i in files:
                threads[i].start()
            for i in files:
                threads[i].join()

            quize = queue.qsize()

            while quize > 0:
                print "下面是 队列，print %d " % (quize)
                intoUrl = queue.get()
                n.isFind(intoUrl)
                cur.close()
                cur = conn.cursor()
                quize = quize - 1
            else:
                print quize
            print '写入完成'
            queue.task_done()
        except:
            cur.close()
        print " the end  "
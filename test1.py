# -*- coding: utf-8 -*-
#! /usr/bin/env python
from selenium import webdriver
import MySQLdb
import time
import random
import re

def lytxt():
    with open("ly.txt")as f:
        keywords = f.readlines()
        conn = MySQLdb.connect(host="10.6.2.121",port=3306,user="root",passwd="root",charset="utf8")
        cur  =conn.cursor()
        for word in keywords:
            cur.execute("INSERT INTO weibo.weixinfc(keyword) VALUES ('%s')"%word)
        cur.close()
        conn.close()
def db():
    conn = MySQLdb.connect(host="10.6.2.121",port=3306,user="root",passwd="root",charset="utf8")
    cur  =conn.cursor()
    cur.execute("SELECT keyword FROM weibo.weixinfc ORDER BY COUNTINT LIMIT 1")
    keyword =cur.fetchall()[0][0]
    # print keyword
    cur.close()
    conn.close()
    return keyword
def crawl():
    keyword=db()

    keyword1 = re.sub(r"\s+",keyword,"")

    # keyword = keyword.encode("utf8")
    print keyword1

    # print urllib2.quote(keyword)
    # driver = webdriver.Firefox()
    # driver = webdriver.PhantomJS()
    # url = u"http://weixin.sogou.com/weixin?type=1&query=%s&ie=utf8&w=01019900&sut=0"% keyword
    # print url
    # driver.get(url)
    # time.sleep(random.randint(5,10))
    print "1"
    # try:
    # print driver.current_url
    # driver.find_element_by_xpath("//div[@id='sogou_vr_11002301_box_0']").click()
    print "2"
    # print driver.current_url
        # all = driver.window_handles
        # driver.switch_to_window(all[1])
    # time.sleep(random.randint(5,10))
        # urls = driver.find_elements_by_xpath("//h4/a")
        # conn = MySQLdb.connect(host="10.6.2.121",port=3306,user="root",passwd="root",charset="utf8")
        # cur  =conn.cursor()
        # for url in urls:
        #     url.click()
        #     win = driver.window_handles
        #     driver.switch_to_window(win[2])
        #     time.sleep(random.randint(5,10))
        #     title = driver.find_element_by_xpath("(//h2[@class='rich_media_title'])[2]").text
        #     date  = driver.find_element_by_xpath("//em[@id='post-date']").text
        #     uri = driver.current_url
        #     content = driver.find_element_by_xpath("//div[@id='js_content']").text
        #     gzh   = driver.find_element_by_xpath("//a[@id='post-user']").text
        #     print title,date
        #     print uri
        #     print content
        #     try:
        #         cur.execute(u"INSERT INTO CARHOME.news(IR_URLNAME,IR_URLTITLE,IR_URLTIME,IR_CONTENT,IR_SRCNAME,IR_GROUPNAME,IR_AUTHORS,IR_CATALOG2,IR_SITENAME) VALUES ('%s','%s','%s','%s','%s','房车微信','%s','房车微信','%s')"%(uri,title,date,content,gzh,gzh,gzh))
        #     except MySQLdb.Error,e:
        #         print '未入库!'
        #         print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        #     driver.close()
        #     win1 = driver.window_handles
        #     driver.switch_to_window(win1[1])
        # cur.execute("UPDATE weibo.weixinfc SET COUNTINT = COUNTINT+1 WHERE keyword='%s'"%keyword)
        # cur.close()
        # conn.close()
    # except:
    #     print u"没有此公众号%s"% keyword
    #     conn = MySQLdb.connect(host="10.6.2.121",port=3306,user="root",passwd="root",charset="utf8")
    #     cur  =conn.cursor()
    #     cur.execute("DELETE FROM weibo.weixinfc WHERE keyword='%s'"%keyword)
    #     cur.close()
    #     conn.close()
    #     driver.quit()
    # driver.quit()
if __name__ =="__main__":
    # while 1:
    #     try:
    #         crawl()
    #         time.sleep(random.randint(5,10))
    #     except:
    #         time.sleep(random.randint(10,15))
    #         continue
    crawl()
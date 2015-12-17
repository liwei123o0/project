# -*- coding: utf-8 -*-
#! /usr/bin/env python
from selenium import webdriver
import time
import MySQLdb
import random
def weixinfc():

    conn = MySQLdb.connect(host="10.6.2.121",port=3306,user="root",passwd="root",charset="utf8")
    cur  =conn.cursor()
    cur.execute("SELECT keyword FROM weibo.weixinfc ORDER BY COUNTINT LIMIT 1")
    url =cur.fetchall()[0][0]
    print url

    driver = webdriver.Firefox()

    driver.get(url)
    time.sleep(random.randint(10,15))
    try:
        urls  =   driver.find_elements_by_xpath("//h4/a").get_attribute("href")

        for url in urls:

            uri = "http://weixin.sogou.com"+url
            print uri
            # driver.get(uri)
            # conten = driver.find_element_by_xpath("//div[@id='js_content']").text
            # date    = driver.find_element_by_xpath("//em[@id='post-date']").text
            #
            # # cur.execute("INSERT INTO weibo.weixinfc (url) VALUES ('%s')"%uri)
            # print conten,date
            # cur.execute("UPDATE weibo.weixinfc SET COUNTINT = COUNTINT+1 WHERE URL='%s'"%url)

            time.sleep(random.randint(5,20))

    except:
        print "异常"
    driver.quit()
    cur.close()
    conn.close()

if __name__=='__main__':
    weixinfc()
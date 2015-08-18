# -*- coding: utf-8 -*-
#! /usr/bin/env python
from mysqlutile import Mysql
import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import MySQLdb
import random
dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["userAgent"] = (
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:37.0) Gecko/20100101 Firefox/37.0"
)

def urlall():
    conn = MySQLdb.connect(host="10.6.2.121",port=3306,user="root",passwd="root",charset="utf8")
    cur  =conn.cursor()
    cur.execute("SELECT URL FROM weibo.weixinurl ORDER BY COUNTINT LIMIT 1")
    url =cur.fetchall()[0][0]
    cur.execute("UPDATE weibo.weixinurl SET COUNTINT = COUNTINT+1 WHERE URL='%s'"%url)
    conn.commit()
    cur.close()
    conn.close()
    return str(url)
def weixinsearch():
    urls =[]
    driver =webdriver.PhantomJS(desired_capabilities=dcap)
    # driver = webdriver.Firefox()
    url =urlall()
    print url
    driver.get(url)
    driver.implicitly_wait(5)
    try:
        driver.find_element_by_xpath("//div[@id='wxmore']/a").click()
    except:
        pass
    jxs   = driver.find_element_by_xpath("//h3[@id='weixinname']").text
    urlse =driver.find_elements_by_xpath("//h4/a")
    for a in urlse:
        a1= a.get_attribute("href")
        a1 = str(a1)
        urls.append(a1)
    cur =Mysql(host="10.6.2.121")
    cur.conDB()
    for uri in urls:
        driver.get(uri)
        time.sleep(random.randint(3,5))
        title = driver.find_element_by_xpath("//h2[@id='activity-name']").text
        date  = driver.find_element_by_xpath("//em[@id='post-date']").text
        conten = driver.find_element_by_xpath("//div[@id='js_content']").text
        urlconten = driver.current_url
        print title,"经销商：",jxs,date,urlconten
        cur.selDB("INSERT INTO weibo.WEIXIN(SCREEN_NAME,DATE_ISSUE,EVENT_TOPIC,EVENT_DESCR,EVENT_URL,SEARCHED_URL) VALUES ('%s','%s','%s','%s','%s','%s')"%(jxs,date,title,conten,urlconten,url))
    cur.closeDB()
    driver.quit()
while 1:
    try:
        weixinsearch()
        print "随机休息"
        time.sleep(random.randint(60,80))
    except:
        print "异常"
        continue
# -*- coding: utf-8 -*-
#! /usr/bin/env python
from selenium import webdriver
import MySQLdb
import time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import re

dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["userAgent"] = (
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:37.0) Gecko/20100101 Firefox/37.0"
)

def urlall():
    conn = MySQLdb.connect(host="10.6.2.121",port=3306,user="root",passwd="root",charset="utf8")
    cur  =conn.cursor()
    cur.execute("SELECT URL FROM weibo.sina_uid ORDER BY COUNTINT LIMIT 1")
    url =cur.fetchall()[0][0]
    cur.execute("UPDATE weibo.sina_uid SET COUNTINT = COUNTINT+1 WHERE URL='%s'"%url)
    conn.commit()
    cur.close()
    conn.close()
    return str(url)

def sinaserachuid():
    url = urlall()
    print url
    driver = webdriver.PhantomJS(desired_capabilities=dcap)
    driver.get("http://s.weibo.com/weibo/%25E5%258D%258E%25E6%2599%25A8%25E4%25B8%25AD%25E5%258D%258E%25E9%2599%2595%25E8%25A5%25BF%25E5%2598%2589%25E6%2581%2592?topnav=1&wvr=6&b=1")
    time.sleep(10)

    driver.find_element_by_xpath("//a[@class='name_txt']").click()
    time.sleep(10)
    hand              = driver.window_handles
    print hand
    driver.switch_to(hand[1])
    html              = driver.find_element_by_xpath("//html")
    # USER_NAME       = driver.find_element_by_xpath("//span[@class='username']").text
    # FOCUS_COUNT     = driver.find_element_by_xpath("(//strong[@class='W_f18'])[1]").text
    # FANS_COUNT      = driver.find_element_by_xpath("(//strong[@class='W_f18'])[2]").text
    # MESSAGE_COUNT   = driver.find_element_by_xpath("(//strong[@class='W_f18'])[3]").text
    # LEVEL           = driver.find_element_by_xpath("//a[@class='W_icon_level icon_level_c3']/span | //a[@class='W_icon_level icon_level_c2']/span  |//a[@class='W_icon_level icon_level_c4']/span").text
    # OCCUPATION      = driver.find_element_by_xpath("(//span[@class='item_text W_fl'])[1]").text
    # Full_USER_NAME  = driver.find_element_by_xpath("//div[@class='pf_intro']").text
    # URL             = driver.current_url()

    CONTENT         = driver.find_elements_by_xpath("//div[@class='WB_text W_f14']")
    TIME            = driver.find_elements_by_xpath("//div[@class='WB_from S_txt2']/a[@class='S_txt2'][1]")
    CONTENT_FROM    = driver.find_elements_by_xpath("//div[@class='WB_from S_txt2']/a[@class='S_txt2'][2]")

    # print FANS_COUNT,FOCUS_COUNT,MESSAGE_COUNT,LEVEL,OCCUPATION,Full_USER_NAME
    print html.text
    driver.quit()
while 1:
    sinaserachuid()
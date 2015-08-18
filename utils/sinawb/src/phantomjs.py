# -*- coding: utf-8 -*-
#! /usr/bin/env python
from selenium import webdriver
import urllib2
import time
def dtwb(keyword):
    data=[]
    driver = webdriver.PhantomJS()
    #URL编码
    keyword =urllib2.quote(keyword)
    driver.get("http://s.weibo.com/weibo/%s&Refer=index"%keyword)
    time.sleep(3)
    #内容获取
    conten = driver.find_element_by_xpath("//p[@class='comment_txt']").text
    conten = conten.encode("utf8")
    #转发数获取
    zfss   = driver.find_elements_by_xpath("(//ul[@class='feed_action_info feed_action_row4']/li[2]//span[@class='line S_line1']//em)")
    zfs =[]
    for i in zfss:
        zfs.append(i.text.encode("utf8"))
    z = sum([int(x) for x in zfs if x ])
    #评论数获取
    plss   = driver.find_elements_by_xpath("(//ul[@class='feed_action_info feed_action_row4']/li[3]//span[@class='line S_line1']//em)")
    pls =[]
    for j in plss:
        pls.append(j.text)
    p = sum([int(xx) for xx in pls if xx])
    #退出浏览器渲染
    driver.quit()
    #内容输出
    # print "内容:\n%s"%conten
    # print "转发总数:%s"%z
    # print "评论总数:%s"%p
    data.append(conten.decode("utf8"))
    data.append(str(z).decode("utf8"))
    data.append(str(p).decode("utf8"))
    return data
#测试
# if __name__=="__main__":
#     dtwb("xcv")
#     for i in dtwb("日本的一家动物园里，喂小熊猫吃苹果有独特的技巧"):
#         print i
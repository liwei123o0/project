# -*- coding: utf-8 -*-
#! /usr/bin/env python
from flask import Flask,jsonify
from selenium import webdriver
import time,re
from mysqlutile import Mysql
# app =Flask(__name__)

# @app.route("/<uid>")
# def user(uid):
#     if uid==int:
#         url=u"http://weibo.com/u/%s"
#     else:
#         url =u"http://weibo.com/%s" % uid
#     conten =weibo(url)
#     if conten=="":
#         return u"无数据"
#     data ={
#         "gzs":conten[0],
#         "fs":conten[1],
#         "wb":conten[2]
#     }
#     return jsonify(data)

def readtxt():
    with open("weibouid.txt","r")as f:
        keys =f.readlines()
    return keys
def weibo():
    urls =readtxt()
    My =Mysql(host="10.6.2.121")
    My.conDB()
    for uri in urls:
        driver =webdriver.Firefox()
        driver.get("http://weibo.com/u/%s"% uri)
        time.sleep(5)
        try:
            url = re.sub("http:\/\/weibo\.com\/","",str(driver.current_url))
            url = re.sub("u\/","",str(url))
            uri = re.sub("\\n","",uri)
            username =driver.find_element_by_xpath("//span[@class='username']").text
            gzs =driver.find_element_by_xpath("(//strong[@class='W_f18'])[1]|(//strong[@class='W_f14'])[1]|(//strong[@class='W_f12'])[1]").text
            fs  =driver.find_element_by_xpath("(//strong[@class='W_f18'])[2]|(//strong[@class='W_f14'])[2]|(//strong[@class='W_f12'])[2]").text
            wb  =driver.find_element_by_xpath("(//strong[@class='W_f18'])[3]|(//strong[@class='W_f14'])[3]|(//strong[@class='W_f12'])[3]").text
            print uri,gzs,fs,wb,url,username
            My.selDB("INSERT INTO echarts.uid(uid,gzs,fs,wb,url,username) VALUES ('%s','%s','%s','%s','%s','%s')"%(uri,gzs,fs,wb,url,username))
            # data =[]
            # data.append(gzs)
            # data.append(fs)
            # data.append(wb)
            driver.close()
            # return data
        except:
            driver.close()
            # return ""
    My.closeDB()
if __name__=="__main__":
    weibo()
    # print readtxt()
#     app.run(host="10.6.2.231",port=80,debug=True)

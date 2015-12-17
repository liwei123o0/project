# -*- coding: utf-8 -*-
#! /usr/bin/env python

def loadword():
    with open("E:\projectall\project\keyword.txt","rb")as f:
        words = f.readlines()
    return words
def mysqlword():
    import MySQLdb
    conn = MySQLdb.connect(host="10.6.2.121",port=3306,user="root",passwd="root",charset="utf8")
    cur  =conn.cursor()
    cur.execute("SELECT keyword FROM weibo.weixinfc")
    words =cur.fetchall()
    cur.close()
    conn.close()
    return words
def joinurl():
    words = loadword()
    # words = mysqlword()
    for word in words:
        word = word.replace("\r\n","")
        url = "".join("http://weixin.sogou.com/weixin?type=2&query=%s&ie=utf8&tsn=1"% word,)
        url1 = "".join("http://weixin.sogou.com/weixin?type=1&query=%s&ie=utf8"% word,)
        print url1
        # with open("url.txt","a+")as w:
        #     w.write(url+"\n")
joinurl()
# print mysqlword()

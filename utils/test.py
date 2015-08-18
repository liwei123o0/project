# -*- coding: utf-8 -*-
#! /usr/bin/env python
import MySQLdb
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
def openfile():
    conn = MySQLdb.connect(host="10.6.2.121",port=3306,user="root",passwd="root",charset="utf8")
    cur  =conn.cursor()
    with open("weixin.txt","r")as f:
        url = f.readlines()
        for i in url:
            print i,
            try:
                cur.execute("INSERT INTO weibo.weixinurl (URL) VALUES ('%s')"%i)
            except:
                continue
        conn.commit()
        cur.close()
        conn.close()
print urlall()
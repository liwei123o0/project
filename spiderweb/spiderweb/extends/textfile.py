# -*- coding: utf-8 -*-
#! /usr/bin/env python

import os.path
import platform
import urllib2
import logging
import MySQLdb
class FileText():

    @classmethod
    def load_config(self,config_path):
        if os.path.exists(config_path):
            path  = os.path.abspath(config_path)
            if platform.system() =="Windows":
                path =path.replace('\\','/')
                path = 'file:///'+path
            else:
                path = 'file://'+path
        try:
            txt = urllib2.urlopen(path,timeout=10).read()

        except:
            logging.WARNING(u"请求配置文件出错！")
            txt =u''
        return txt
    @classmethod
    def loadkeyword(self):
        conn = MySQLdb.connect(host="10.6.2.121",user="root",passwd="root",port=3306,charset="utf8")
        cur = conn.cursor()
        cur.execute("SELECT keyword FROM weibo.keyword_fenxi ORDER BY countint LIMIT 1")
        word =cur.fetchall()[0][0].encode("utf8")
        cur.execute("UPDATE weibo.keyword_fenxi SET countint = countint+1 WHERE keyword='%s'"%word)
        conn.commit()
        cur.close()
        conn.close()
        return word


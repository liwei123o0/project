# -*- coding: utf-8 -*-
#! /usr/bin/env python
'''
mysql数据库操作，依赖包可以通过   下载然后导入
'''
import MySQLdb
u'''
自己封装的mysql工具类，有5个方法:
1.连接数据库方法conDB()
2.查询数据库方法selcetDB()
3.关闭数据库方法closeDB()
'''
class Mysql(object):

    def __init__(self,port=3306,host=u'127.0.0.1',user=u'root',passwd=u'root',db=u'', charset='utf8'):
        self.host = host
        self.user =user
        self.passwd =passwd
        self.db = db
        self.port   =port
        self.charset =charset
    def conDB(self):
        try:
            self.conn =MySQLdb.connect(host=self.host,user=self.user,passwd=self.passwd,db=self.db,port=self.port,charset=self.charset)
            self.cur =self.conn.cursor()
            # print "ok"
        except:
            print(u'无法连接到数据库!')
    def selDB(self,select):
        try:
            self.cur.execute(select)
            # self.cur.fetchall()
            self.conn.commit()
            # print "okok"
        except MySQLdb.Error,e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
            # self.conn.rollback()
    def closeDB(self):
        try:
            self.cur.close()
            self.conn.close()
        except:
            print(u'数据库关闭异常!')

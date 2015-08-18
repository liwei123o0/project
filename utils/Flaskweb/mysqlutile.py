# -*- coding: utf-8 -*-
'''
mysql数据库操作，依赖包可以通过   下载然后导入
'''
import MySQLdb
import time
import threading
u'''
自己封装的mysql工具类，有5个方法:
1.连接数据库方法conDB()
2.查询数据库方法selcetDB()
3.关闭数据库方法closeDB()
'''
class Mysql(object):

    def __init__(self,port=3306,host=u'127.0.0.1',user=u'root',passwd=u'root',db=u''):
        self.host = host
        self.user =user
        self.passwd =passwd
        self.db = db
        self.port   =port
    def conDB(self):
        try:
            self.conn =MySQLdb.connect(host=self.host,user=self.user,passwd=self.passwd,db=self.db,port=self.port)
            self.cur =self.conn.cursor()
        except:
            print(u'无法连接到数据库!')
    def selDB(self,select):
        try:
            self.cur.execute(select)
        except:
            print u"查询数据库失败异常！"
        return self.cur.fetchall()
    def closeDB(self):
        try:
            self.cur.close()
            self.conn.close()
        except:
            print(u'数据库关闭异常!')

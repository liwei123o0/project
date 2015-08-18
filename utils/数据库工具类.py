# -*- coding: utf-8 -*-
'''
mysql数据库操作，依赖包可以通过 esay_install MySQL-python 下载然后导入
'''
import MySQLdb
u'''
自己封装的mysql工具类，有5个方法:
1.连接数据库方法conDB()
2.查询数据库方法selcetDB()
3.插入数据库方法inserDB()
4.更新数据库方法updateDB()
5.关闭数据库方法closeDB()
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
            print self.conn
            self.cur =self.conn.cursor()
            print self.cur
        except:
            print('无法连接到数据库!')
    def selDB(self):
        while True:
            sql_ku =raw_input(u'请输入要查的数据库库名，输入‘exit’则退出查询（如：test）')
            if sql_ku == u'':
                print(u'输入的库名为空，请重新输入！')
                continue
            elif sql_ku == u'exit':
                print(u'已成功退出！')
                break
            else:
                pass
            sql_biao =raw_input(u'请输入要查的数据库表名，输入‘exit’则退出查询（如：user）')
            if sql_biao == u'':
                print(u'输入的表明为空，请重新输入！')
                continue
            if sql_biao ==u'exit':
                print(u'已成功退出！')
                break
            else:
                print u'你输入的数据库库名为%s,表名%s'%(sql_ku,sql_biao)
                try:
                    self.cur.execute(u'SELECT * FROM %s.%s'%(sql_ku,sql_biao))
                    print(self.cur.fetchall())
                except:
                    print(u'输入的数据库有误，程序退出！')
                    break

    def inserDB(self):
        while True:

            ins =raw_input(u'请输入要插入表的表名（不为空，库名与表明中间以.隔开或输入‘exit’退出）：')
            if ins ==u'':
                print(u'不能为空，请重新输入！')
                continue
            elif ins ==u'exit':
                print(u'退出成功！')
                break
            else:
                print(u'你要插入的库名及表名为：%s'%ins)
            value1 = int(raw_input(u'请输入要插入的id值：'))
            if value1 == u'':
                print(u'id不能为空，请重新输入！')
                continue
            elif value1 ==u'exit':
                print(u'退出成功')
                break
            else:
                print(u'你要输入的id值为：%s'%value1)
            value2 = raw_input(u'请输入要插入的name值：')
            if value2 == u'':
                print(u'name不能为空，请重新输入！')
                continue
            elif value2 ==u'exit':
                print(u'退出成功')
                break
            else:
                print(u'你要输入的id值为：%s'%value2)

            insql = u"INSERT INTO %s VALUES(%d,'%s')"%(ins,value1,value2)
            try:
                self.cur.execute(insql)
                self.conn.commit()
                break
            except:
                print(u'插入的数据有误！')
                self.conn.rollback()
                break

    def updateDB(self,upsql):
        self.upsql = upsql

        try:
            self.cur.execute(self.upsql)
            self.conn.commit()
        except:
            print(u'输入的sql语句有误请重新输入')

    def closeDB(self):
        try:
            self.cur.close()
            self.conn.close()
        except:
            print(u'数据库关闭异常!')
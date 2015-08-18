# -*- coding: utf-8 -*-
#! /usr/bin/env python
from mysqlutile import Mysql
import time
u'''
查询入库量py
1.mysqlday()方法    //查询每天的总入库量
2.mysqlweek()方法   //查询上周的总入库量
3.mysqlmonth()方法  //查询上月的总入库量
4.mysqlyear()方法   //查询今年的总入库量
'''

#查询每天的总入库量
def mysqlday():
    m = Mysql(host="10.6.2.121")
    m.conDB()
    news =  m.selDB("SELECT COUNT(*) FROM scrapy.news WHERE DATE_SUB(CURDATE(), INTERVAL 0 DAY) = date(INSERT_TIME); ")[0][0]
    bbs =   m.selDB("SELECT COUNT(*) FROM scrapy.bbs WHERE DATE_SUB(CURDATE(), INTERVAL 0 DAY) = date(INSERT_TIME); ")[0][0]
    sina =  m.selDB("SELECT COUNT(*) FROM weibo.sina WHERE DATE_SUB(CURDATE(), INTERVAL 0 DAY) = date(INSERT_TIME);")[0][0]
    number = news+bbs+sina
    print number
    # m.selDB("INSERT INTO echarts.user(TYPE,SQLNUM) VALUES('ALLDAY','%s')"%number)
    m.selDB("UPDATE echarts.user SET SQLNUM='%s' WHERE TYPE='ALLDAY'"% number)
    m.closeDB()
#查询上周的总入库量
def mysqlweek():
    m = Mysql(host="10.6.2.121")
    m.conDB()
    news =  m.selDB("SELECT COUNT(*) FROM scrapy.news WHERE YEARWEEK(date_format(INSERT_TIME,'%Y-%m-%d')) = YEARWEEK(now())-1; ")[0][0]
    bbs =   m.selDB("SELECT COUNT(*) FROM scrapy.bbs WHERE YEARWEEK(date_format(INSERT_TIME,'%Y-%m-%d')) = YEARWEEK(now())-1;")[0][0]
    sina =  m.selDB("SELECT COUNT(*) FROM weibo.sina WHERE YEARWEEK(date_format(INSERT_TIME,'%Y-%m-%d')) = YEARWEEK(now())-1;")[0][0]
    number = news+bbs+sina
    print number
    # m.selDB("INSERT INTO echarts.user(TYPE,SQLNUM) VALUES('ALLWEEK','%s')"%number)
    m.selDB("UPDATE echarts.user SET SQLNUM='%s' WHERE TYPE='ALLWEEK'"% number)
    m.closeDB()
#查询上月的总入库量
def mysqlmonth():
    m = Mysql(host="10.6.2.121")
    m.conDB()
    news =  m.selDB("SELECT COUNT(*) FROM scrapy.news WHERE DATE_FORMAT(INSERT_TIME,'%Y-%m')=DATE_FORMAT(DATE_SUB(curdate(), INTERVAL 1 MONTH),'%Y-%m'); ")[0][0]
    bbs =   m.selDB("SELECT COUNT(*) FROM scrapy.bbs WHERE DATE_FORMAT(INSERT_TIME,'%Y-%m')=DATE_FORMAT(DATE_SUB(curdate(), INTERVAL 1 MONTH),'%Y-%m');")[0][0]
    sina =  m.selDB("SELECT COUNT(*) FROM weibo.sina WHERE DATE_FORMAT(INSERT_TIME,'%Y-%m')=DATE_FORMAT(DATE_SUB(curdate(), INTERVAL 1 MONTH),'%Y-%m');")[0][0]
    number = news+bbs+sina
    print number
    # m.selDB("INSERT INTO echarts.user(TYPE,SQLNUM) VALUES('ALLMONTH','%s')"%number)
    m.selDB("UPDATE echarts.user SET SQLNUM='%s' WHERE TYPE='ALLMONTH'"% number)
    m.closeDB()
#查询今年的总入库量
def mysqlyear():
    m = Mysql(host="10.6.2.121")
    m.conDB()
    news =  m.selDB("SELECT COUNT(*) FROM scrapy.news WHERE YEAR(date_format(INSERT_TIME,'%Y-%m-%d')) = YEAR(now()); ")[0][0]
    bbs =   m.selDB("SELECT COUNT(*) FROM scrapy.bbs WHERE YEAR(date_format(INSERT_TIME,'%Y-%m-%d')) = YEAR(now());")[0][0]
    sina =  m.selDB("SELECT COUNT(*) FROM scrapy.bbs WHERE YEAR(date_format(INSERT_TIME,'%Y-%m-%d')) = YEAR(now());")[0][0]
    number = news+bbs+sina
    print number
    # m.selDB("INSERT INTO echarts.user(TYPE,SQLNUM) VALUES('ALLYEAR','%s')"%number)
    m.selDB("UPDATE echarts.user SET SQLNUM='%s' WHERE TYPE='ALLYEAR'"% number)
    m.closeDB()
#查询今年news的总入库量
def mysqlyearnews():
    m = Mysql(host="10.6.2.121")
    m.conDB()
    news =  m.selDB("SELECT COUNT(*) FROM scrapy.news WHERE YEAR(date_format(INSERT_TIME,'%Y-%m-%d')) = YEAR(now()); ")[0][0]
    number = news
    print number
    # m.selDB("INSERT INTO echarts.user(TYPE,SQLNUM) VALUES('ALLYEARNEWS','%s')"%number)
    m.selDB("UPDATE echarts.user SET SQLNUM='%s' WHERE TYPE='ALLYEARNEWS'"% number)
    m.closeDB()
#查询每天news的总入库量
def mysqldaynews():
    m = Mysql(host="10.6.2.121")
    m.conDB()
    news =  m.selDB("SELECT COUNT(*) FROM scrapy.news WHERE DATE_SUB(CURDATE(), INTERVAL 0 DAY) = date(INSERT_TIME); ")[0][0]
    number = news
    print number
    # m.selDB("INSERT INTO echarts.user(TYPE,SQLNUM) VALUES('ALLDAYNEWS','%s')"%number)
    m.selDB("UPDATE echarts.user SET SQLNUM='%s' WHERE TYPE='ALLDAYNEWS'"% number)
    m.closeDB()
#查询上周news的总入库量
def mysqlweeknews():
    m = Mysql(host="10.6.2.121")
    m.conDB()
    news =  m.selDB("SELECT COUNT(*) FROM scrapy.news WHERE YEARWEEK(date_format(INSERT_TIME,'%Y-%m-%d')) = YEARWEEK(now())-1; ")[0][0]
    number = news
    print number
    # m.selDB("INSERT INTO echarts.user(TYPE,SQLNUM) VALUES('ALLWEEKNEWS','%s')"%number)
    m.selDB("UPDATE echarts.user SET SQLNUM='%s' WHERE TYPE='ALLWEEKNEWS'"% number)
    m.closeDB()
#查询上月news的总入库量
def mysqlmonthnews():
    m = Mysql(host="10.6.2.121")
    m.conDB()
    news =  m.selDB("SELECT COUNT(*) FROM scrapy.news WHERE DATE_FORMAT(INSERT_TIME,'%Y-%m')=DATE_FORMAT(DATE_SUB(curdate(), INTERVAL 1 MONTH),'%Y-%m'); ")[0][0]
    number = news
    print number
    # m.selDB("INSERT INTO echarts.user(TYPE,SQLNUM) VALUES('ALLMONTHNEWS','%s')"%number)
    m.selDB("UPDATE echarts.user SET SQLNUM='%s' WHERE TYPE='ALLMONTHNEWS'"% number)
    m.closeDB()
#查询今年bbs的总入库量
def mysqlyearbbs():
    m = Mysql(host="10.6.2.121")
    m.conDB()
    bbs =  m.selDB("SELECT COUNT(*) FROM scrapy.bbs WHERE YEAR(date_format(INSERT_TIME,'%Y-%m-%d')) = YEAR(now()); ")[0][0]
    number = bbs
    print number
    # m.selDB("INSERT INTO echarts.user(TYPE,SQLNUM) VALUES('ALLYEARBBS','%s')"%number)
    m.selDB("UPDATE echarts.user SET SQLNUM='%s' WHERE TYPE='ALLYEARBBS'"% number)
    m.closeDB()
#查询每天bbs的总入库量
def mysqldaybbs():
    m = Mysql(host="10.6.2.121")
    m.conDB()
    bbs =  m.selDB("SELECT COUNT(*) FROM scrapy.bbs WHERE DATE_SUB(CURDATE(), INTERVAL 0 DAY) = date(INSERT_TIME); ")[0][0]
    number = bbs
    print number
    # m.selDB("INSERT INTO echarts.user(TYPE,SQLNUM) VALUES('ALLDAYBBS','%s')"%number)
    m.selDB("UPDATE echarts.user SET SQLNUM='%s' WHERE TYPE='ALLDAYBBS'"% number)
    m.closeDB()
#查询上周bbs的总入库量
def mysqlweekbbs():
    m = Mysql(host="10.6.2.121")
    m.conDB()
    bbs =  m.selDB("SELECT COUNT(*) FROM scrapy.bbs WHERE YEARWEEK(date_format(INSERT_TIME,'%Y-%m-%d')) = YEARWEEK(now())-1; ")[0][0]
    number = bbs
    print number
    # m.selDB("INSERT INTO echarts.user(TYPE,SQLNUM) VALUES('ALLWEEKBBS','%s')"%number)
    m.selDB("UPDATE echarts.user SET SQLNUM='%s' WHERE TYPE='ALLWEEKBBS'"% number)
    m.closeDB()
#查询上月bbs的总入库量
def mysqlmonthbbs():
    m = Mysql(host="10.6.2.121")
    m.conDB()
    bbs =  m.selDB("SELECT COUNT(*) FROM scrapy.bbs WHERE DATE_FORMAT(INSERT_TIME,'%Y-%m')=DATE_FORMAT(DATE_SUB(curdate(), INTERVAL 1 MONTH),'%Y-%m'); ")[0][0]
    number = bbs
    print number
    # m.selDB("INSERT INTO echarts.user(TYPE,SQLNUM) VALUES('ALLMONTHBBS','%s')"%number)
    m.selDB("UPDATE echarts.user SET SQLNUM='%s' WHERE TYPE='ALLMONTHBBS'"% number)
    m.closeDB()
#查询今年sina的总入库量
def mysqlyearsina():
    m = Mysql(host="10.6.2.121")
    m.conDB()
    sina =  m.selDB("SELECT COUNT(*) FROM weibo.sina WHERE YEAR(date_format(INSERT_TIME,'%Y-%m-%d')) = YEAR(now()); ")[0][0]
    number = sina
    print number
    # m.selDB("INSERT INTO echarts.user(TYPE,SQLNUM) VALUES('ALLYEARSINA','%s')"%number)
    m.selDB("UPDATE echarts.user SET SQLNUM='%s' WHERE TYPE='ALLYEARSINA'"% number)
    m.closeDB()
#查询每天sina的总入库量
def mysqldaysina():
    m = Mysql(host="10.6.2.121")
    m.conDB()
    sina =  m.selDB("SELECT COUNT(*) FROM weibo.sina WHERE DATE_SUB(CURDATE(), INTERVAL 0 DAY) = date(INSERT_TIME); ")[0][0]
    number = sina
    print number
    # m.selDB("INSERT INTO echarts.user(TYPE,SQLNUM) VALUES('ALLDAYSINA','%s')"%number)
    m.selDB("UPDATE echarts.user SET SQLNUM='%s' WHERE TYPE='ALLDAYSINA'"% number)
    m.closeDB()
#查询上周sina的总入库量
def mysqlweeksina():
    m = Mysql(host="10.6.2.121")
    m.conDB()
    sina =  m.selDB("SELECT COUNT(*) FROM weibo.sina WHERE YEARWEEK(date_format(INSERT_TIME,'%Y-%m-%d')) = YEARWEEK(now())-1; ")[0][0]
    number = sina
    print number
    # m.selDB("INSERT INTO echarts.user(TYPE,SQLNUM) VALUES('ALLWEEKSINA','%s')"%number)
    m.selDB("UPDATE echarts.user SET SQLNUM='%s' WHERE TYPE='ALLWEEKSINA'"% number)
    m.closeDB()
#查询上月sina的总入库量
def mysqlmonthsina():
    m = Mysql(host="10.6.2.121")
    m.conDB()
    sina =  m.selDB("SELECT COUNT(*) FROM weibo.sina WHERE DATE_FORMAT(INSERT_TIME,'%Y-%m')=DATE_FORMAT(DATE_SUB(curdate(), INTERVAL 1 MONTH),'%Y-%m'); ")[0][0]
    number = sina
    print number
    # m.selDB("INSERT INTO echarts.user(TYPE,SQLNUM) VALUES('ALLMONTHSINA','%s')"%number)
    m.selDB("UPDATE echarts.user SET SQLNUM='%s' WHERE TYPE='ALLMONTHSINA'"% number)
    m.closeDB()
#查询三十天数据
def data30():
    m = Mysql(host="10.6.2.121")
    m.conDB()
    m.selDB("DELETE FROM echarts.user  WHERE TYPE LIKE '%TIME%'")
    for i in xrange(0,30):
        timedata = m.selDB("SELECT DATE_SUB(CURDATE(), INTERVAL %s DAY)"% i)[0][0]
        daynews  = m.selDB("SELECT COUNT(*) FROM scrapy.news where date(INSERT_TIME)=DATE_SUB(CURDATE(), INTERVAL %s DAY)"% i)[0][0]
        daybbs   = m.selDB("SELECT COUNT(*) FROM scrapy.bbs where date(INSERT_TIME)=DATE_SUB(CURDATE(), INTERVAL %s DAY)"% i)[0][0]
        daysina  = m.selDB("SELECT COUNT(*) FROM weibo.sina where date(INSERT_TIME)=DATE_SUB(CURDATE(), INTERVAL %s DAY)"% i)[0][0]
        day      = daynews+daybbs+daysina
        #插入30天数据量
        m.selDB("INSERT INTO echarts.user(TYPE,SQLNUM,DAY_TIME) VALUES ('TIMEDAYNEWS','%s','%s')"%(daynews,timedata))
        m.selDB("INSERT INTO echarts.user(TYPE,SQLNUM,DAY_TIME) VALUES ('TIMEDAYBBS','%s','%s')"%(daybbs,timedata))
        m.selDB("INSERT INTO echarts.user(TYPE,SQLNUM,DAY_TIME) VALUES ('TIMEDAYSINA','%s','%s')"%(daysina,timedata))
        m.selDB("INSERT INTO echarts.user(TYPE,SQLNUM,DAY_TIME) VALUES ('TIMEDAY','%s','%s')"%(day,timedata))
        #更新30天数据量
        # m.selDB("UPDATE echarts.user SET SQLNUM='%s',DAY_TIME='%s' WHERE TYPE='TIMEDAYNEWS' AND date(DAY_TIME)<=DATE_SUB(CURDATE(), INTERVAL %d DAY) LIMIT 1"%(daynews,time,i))
        # m.selDB("UPDATE echarts.user SET SQLNUM='%s',DAY_TIME='%s' WHERE TYPE='TIMEDAYBBS' AND date(DAY_TIME)<=DATE_SUB(CURDATE(), INTERVAL %d DAY) LIMIT 1"%(daybbs,time,i))
        # m.selDB("UPDATE echarts.user SET SQLNUM='%s',DAY_TIME='%s' WHERE TYPE='TIMEDAYSINA' AND date(DAY_TIME)<=DATE_SUB(CURDATE(), INTERVAL %d DAY) LIMIT 1"%(daysina,time,i))
        # m.selDB("UPDATE echarts.user SET SQLNUM='%s',DAY_TIME='%s' WHERE TYPE='TIMEDAY' AND date(DAY_TIME)<=DATE_SUB(CURDATE(), INTERVAL %d DAY) LIMIT 1"%(day,time,i))
        print timedata,daynews,daybbs,daysina,day
    m.closeDB()
def main():
    mysqlday()
    mysqlweek()
    mysqlmonth()
    mysqlyear()
    mysqldaynews()
    mysqlweeknews()
    mysqlmonthnews()
    mysqlyearnews()
    mysqldaybbs()
    mysqlweekbbs()
    mysqlmonthbbs()
    mysqlyearbbs()
    mysqldaysina()
    mysqlweeksina()
    mysqlmonthsina()
    mysqlyearsina()
    data30()
#测试
if __name__=="__main__":
    main()
    # data30()
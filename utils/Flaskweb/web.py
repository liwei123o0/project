# -*- coding: utf-8 -*-
#! /usr/bin/env python
from flask import Flask,render_template,jsonify
from mysqlutile import Mysql
app = Flask(__name__)

#十分钟实时数据
@app.route("/mysqlsel",methods=["GET","POST"])
def get():
    a = selmysql()
    ssnews = a[0]
    ssbbs  = a[1]
    sszl   = a[2]
    sssina = a[3]
    ssweixin=a[4]
    data ={
        "ssnews":"%s"%ssnews,
        "ssbbs" :"%s"%ssbbs,
        "sssina":"%s"%sssina,
        "ssweixin":"%s"%ssweixin,
        "sszl"  :"%s"%sszl
        }
    return jsonify(data)
@app.route("/")
def index():
    return render_template("index.html")
@app.route("/jk")
def JKmysql():
    return render_template("mysqlmini.html")
@app.route("/zl")
def ZLmysql():
    return render_template("mysql.html")
@app.route("/mysqljk")
def mysqljk():
    return render_template("mysqljk.html")
@app.route("/lsdata")
def monthdata():
    return render_template("lsdata.html")
@app.route("/test")
def top():
    return render_template("test.html")
#实时10分钟数据入库量
def selmysql():
    data =[]
    ssnews=[]
    ssbbs =[]
    sssina=[]
    ssweixin=[]
    My = Mysql(host="10.6.2.121")
    My.conDB()
    My1 = Mysql(host="10.6.2.79",user="root",passwd="123@asd")
    My1.conDB()
    for i in range(10,110,10):
        rkl= My.selDB(u"SELECT COUNT(*) FROM scrapy.news WHERE INSERT_TIME>=NOW()-INTERVAL %d MINUTE AND  INSERT_TIME< NOW() - INTERVAL %d MINUTE"%(i,i-10))[0][0]
        ssnews.append(int(rkl))
    for i in range(10,110,10):
        rkl= My.selDB(u"SELECT COUNT(*) FROM scrapy.bbs WHERE INSERT_TIME>=NOW()-INTERVAL %d MINUTE AND  INSERT_TIME< NOW() - INTERVAL %d MINUTE"%(i,i-10))[0][0]
        ssbbs.append(int(rkl))
    for i in range(10,110,10):
        rkl= My.selDB(u"SELECT COUNT(*) FROM weibo.sina WHERE INSERT_TIME>=NOW()-INTERVAL %d MINUTE AND  INSERT_TIME< NOW() - INTERVAL %d MINUTE"%(i,i-10))[0][0]
        sssina.append(int(rkl))
    for i in range(10,110,10):
        rkl= My1.selDB(u"SELECT COUNT(*) FROM WEBSITE_WEIXIN.WEIXIN WHERE STORE_TIME>=NOW()-INTERVAL %d MINUTE AND  STORE_TIME< NOW() - INTERVAL %d MINUTE"%(i,i-10))[0][0]
        ssweixin.append(int(rkl))
    My.closeDB()
    My1.closeDB()
    sszl = [ssnews[i] + ssbbs[i] +sssina[i] + ssweixin[i] for i in xrange(min(len(ssnews),len(ssbbs)))]
    data.append(ssnews)
    data.append(ssbbs)
    data.append(sszl)
    data.append(sssina)
    data.append(ssweixin)
    return data
#获取当天总入库量
@app.route("/mysql",methods=["GET","POST"])
def mysql():
    sql = Mysql(host="10.6.2.121")
    sql.conDB()
    #获取当天入库量
    allnews = sql.selDB(u"SELECT SQLNUM FROM echarts.user WHERE TYPE='ALLDAYNEWS'")[0][0]
    allbbs  = sql.selDB(u"SELECT SQLNUM FROM echarts.user WHERE TYPE='ALLDAYBBS'")[0][0]
    allsina = sql.selDB(u"SELECT SQLNUM FROM echarts.user WHERE TYPE='ALLDAYSINA'")[0][0]
    all     = sql.selDB(u"SELECT SQLNUM FROM echarts.user WHERE TYPE='ALLDAY'")[0][0]
    #获取上周入库量
    allweeknews = sql.selDB(u"SELECT SQLNUM FROM echarts.user WHERE TYPE='ALLWEEKNEWS'")[0][0]
    allweekbbs  = sql.selDB(u"SELECT SQLNUM FROM echarts.user WHERE TYPE='ALLWEEKBBS'")[0][0]
    allweeksina  = sql.selDB(u"SELECT SQLNUM FROM echarts.user WHERE TYPE='ALLWEEKSINA'")[0][0]
    allweek     = sql.selDB(u"SELECT SQLNUM FROM echarts.user WHERE TYPE='ALLWEEK'")[0][0]
    #获取上月入库量
    allmonthnews = sql.selDB(u"SELECT SQLNUM FROM echarts.user WHERE TYPE='ALLMONTHNEWS'")[0][0]
    allmonthbbs  = sql.selDB(u"SELECT SQLNUM FROM echarts.user WHERE TYPE='ALLMONTHBBS'")[0][0]
    allmonthsina  = sql.selDB(u"SELECT SQLNUM FROM echarts.user WHERE TYPE='ALLMONTHSINA'")[0][0]
    allmonth     = sql.selDB(u"SELECT SQLNUM FROM echarts.user WHERE TYPE='ALLMONTH'")[0][0]
    #获取当年入库总量
    allyearnews = sql.selDB(u"SELECT SQLNUM FROM echarts.user WHERE TYPE='ALLYEARNEWS'")[0][0]
    allyearbbs  = sql.selDB(u"SELECT SQLNUM FROM echarts.user WHERE TYPE='ALLYEARBBS'")[0][0]
    allyearsina  = sql.selDB(u"SELECT SQLNUM FROM echarts.user WHERE TYPE='ALLYEARSINA'")[0][0]
    allyear     = sql.selDB(u"SELECT SQLNUM FROM echarts.user WHERE TYPE='ALLYEAR'")[0][0]
    data={
        "allrkl":"[%s,%s,%s,%s]"%(allnews,allbbs,allsina,all),
        "allweek":"[%s,%s,%s,%s]"%(allweeknews,allweekbbs,allweeksina,allweek),
        "allmonth":"[%s,%s,%s,%s]"%(allmonthnews,allmonthbbs,allmonthsina,allmonth),
        "allyear":"[%s,%s,%s,%s]"%(allyearnews,allyearbbs,allyearsina,allyear)
        }
    sql.closeDB()
    return jsonify(data)
@app.route("/day30",methods=["GET","POST"])
def day30():
    sql = Mysql(host="10.6.2.121")
    sql.conDB()
    #获取news三十天数据
    news30=[]
    bbs30=[]
    sina30=[]
    all30=[]
    day30=[]
    for i in xrange(0,30):
        news = sql.selDB(u"SELECT SQLNUM FROM echarts.user WHERE TYPE='TIMEDAYNEWS' AND date(DAY_TIME)=DATE_SUB(CURDATE(), INTERVAL %d DAY)"% i)[0][0]
        news30.append(int(news))
        bbs = sql.selDB(u"SELECT SQLNUM FROM echarts.user WHERE TYPE='TIMEDAYBBS' AND date(DAY_TIME)=DATE_SUB(CURDATE(), INTERVAL %d DAY)"% i)[0][0]
        bbs30.append(int(bbs))
        sina = sql.selDB(u"SELECT SQLNUM FROM echarts.user WHERE TYPE='TIMEDAYSINA' AND date(DAY_TIME)=DATE_SUB(CURDATE(), INTERVAL %d DAY)"% i)[0][0]
        sina30.append(int(sina))
        all = sql.selDB(u"SELECT SQLNUM FROM echarts.user WHERE TYPE='TIMEDAY' AND date(DAY_TIME)=DATE_SUB(CURDATE(), INTERVAL %d DAY)"% i)[0][0]
        all30.append(int(all))
        daytime =str(sql.selDB("SELECT DATE_SUB(CURDATE(), INTERVAL %s DAY)"% i)[0][0])
        day30.append(daytime)
    news30.reverse()
    bbs30.reverse()
    sina30.reverse()
    all30.reverse()
    day30.reverse()
    data={
        "news30":"%s"%news30,
        "bbs30":"%s"% bbs30,
        "sina30":"%s"%sina30,
        "all30":"%s"%all30,
        "day30":"%s"%day30
    }
    sql.closeDB()
    return jsonify(data)
if __name__ =="__main__":
    app.run(host="0.0.0.0",port=80,debug=True)
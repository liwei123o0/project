#! /usr/bin/env python
# -*- coding:utf-8 -*-
import urllib
import urllib2
import cookielib
import re
from lxml import etree
import MySQLdb
import time,datetime

#获取数据库关键词
def db():
    try:
        conn = MySQLdb.connect(host="10.6.2.121",port=3306,user="root",passwd="root",charset="utf8")
        cur  =conn.cursor()
        cur.execute("SELECT keyword FROM weibo.keyword ORDER BY COUNTINT LIMIT 1")
        keyword =cur.fetchall()[0][0]
        cur.close()
        conn.close()
        return keyword
    except:
        return "获取数据库关键词错误，请检查数据库网络连接是否有问题！"

#模拟登陆http://sm.viewslive.cn并进入搜索页面根据关键词来抓取微博信息。
def posturllib(user='',passwd='',wtype='',keyword='',types=''):

    cout =1
    #登录的主页面
    hosturl = 'http://sm.viewslive.cn/login.php' #自己填写

    #设置一个cookie处理器，它负责从服务器下载cookie到本地，并且在发送请求时带上本地的cookie
    cj = cookielib.LWPCookieJar()
    cookie_support = urllib2.HTTPCookieProcessor(cj)
    opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
    urllib2.install_opener(opener)

    #打开登录主页面（他的目的是从页面下载cookie，这样我们在再送post数据时就有cookie了，否则发送不成功）
    h = urllib2.urlopen(hosturl)

    #构造header，一般header至少要包含一下两项。这两项是从抓到的包里分析得出的。
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
               'Referer' : 'http://sm.viewslive.cn/login.php'
               }
    #构造Post数据，他也是从抓大的包里分析得出的。
    postData = {
                'password':'%s'%passwd,
                'username':'%s'%user,
                # 'password':'shanxi03',
                # 'username':'sx1234'
                }
    data = {
        'keyword':'%s'%keyword,
        'page':'1',
        'channel_types':"%s"%types,
        'wtype':"%s"%wtype,
    }
    #连接数据库
    conn = MySQLdb.connect(host="10.6.2.121",port=3306,user="root",passwd="root",charset="utf8")
    cur  =conn.cursor()

    #需要给Post数据编码
    postData = urllib.urlencode(postData)
    data = urllib.urlencode(data)
    #通过urllib2提供的request方法来向指定Url发送我们构造的数据，并完成登录过程
    request = urllib2.Request(hosturl, postData, headers)
    urllib2.urlopen(request)
    html = urllib2.urlopen("http://sm.viewslive.cn/search_ajax.php",data,timeout=10).read()
    html = html.decode("utf8")
    #将HTML解析成dom树
    dom = etree.HTML(html)
    for i in dom.xpath("//div[contains(@class,'WB_feed_type')]"):
        users = "".join(i.xpath(".//a[@class='bold pop-over']/text()"))
        contens = "".join(i.xpath(".//div[@class='weibomsg fl']//text() |.//div[@class='zhuanfa_div2 fl']//text()"))
        times = "".join(i.xpath(".//ul[@class='detailFooter fl']/li/a/text()"))
        urls  = "".join(i.xpath(".//ul[@class='detailFooter fl']/li/a/@href"))
        zfs   = "".join(i.xpath(".//ul[@class='detailFooter fr']/li[1]/text()"))
        pls   = "".join(i.xpath(".//ul[@class='detailFooter fr']/li[2]/text()"))
        imgurl= "".join(i.xpath(".//img[@class='ch-image img-avatar']/@src"))

        #格式化数据
        content = contens.replace("\r\n","").replace("\t","")
        zfs = re.sub("\D+","",zfs)
        pls = re.sub("\D+","",pls)
        uid = re.sub("\D+","",urls)
        mid = re.sub("http.*\/","",urls)
        time = times.encode("utf8")
        month = int(re.findall("[0-9]+",time)[0])
        if month > datetime.datetime.now().month:
            time = "2015-"+time.replace("月","-").replace("年","-").replace("日","")
        else:
            time = "2016-"+time.replace("月","-").replace("年","-").replace("日","")
        # 采集入库
        try:
            time = time.decode("utf8")
            cur.execute(u"INSERT INTO weibo.sina(IR_UID,IR_MID,IR_CREATED_AT,IR_STATUS_CONTENT,IR_RTTCOUNT,IR_GROUPNAME,IR_SITENAME,KEYWORD,IR_SCREEN_NAME,IR_PROFILE_IMAGE_URL) VALUES ('%s','%s','%s','%s','%s','python新浪微博','新浪微博','%s','%s','%s')"%(uid,mid,time,content,zfs,keyword.decode("utf8"),users,imgurl))
        except MySQLdb.Error,e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        #打印相关数据
        print "#############%s#############"%cout
        print u"url:"+urls
        print u"imgurl:"+imgurl
        print u"uid:"+uid
        print u"mid:"+mid
        print u"keyword:"+keyword.decode("utf8")
        print u"时间:"+time
        print u"用户:"+users
        print u"内容:"+content
        print u"转发数:"+zfs
        print u"评论数:"+pls
        #计数器
        cout +=1
    cur.close()
    conn.close()
def update(keyword):
    conn = MySQLdb.connect(host="10.6.2.121",port=3306,user="root",passwd="root",charset="utf8")
    cur  =conn.cursor()
    keyword = keyword.decode("utf8")
    cur.execute(u"UPDATE weibo.keyword SET COUNTINT = COUNTINT+1 WHERE keyword='%s'"%keyword)
    print u"关键词：'"+keyword+u"' 更新成功！"
    cur.close()
    conn.close()


if __name__ =="__main__":
    #用户名
    user = 'hebei03'
    #密码
    passwd = 'hb1234'
    #wtype类型为1为按时间顺序抓取原创微博，类型为空按时间顺序抓取微博信息
    wtype ='1'
    #微博类型(1为新浪微博；2为腾讯微博；5为Twitter)
    types='1'

    while 1:
        #获取搜索微博关键词
        try:
            keyword = db().encode("utf8")
        except:
            time.sleep(3)
            continue
        #根据相关参数抓取微博信息
        try:
            posturllib(user=user,passwd=passwd,wtype=wtype,keyword=keyword,types=types)
        except:
            print "采集异常！"
            time.sleep(3)
            print "重试采集..."
            continue
        #完成后更新数据库关键词
        try:
            update(keyword)
        except:
            print "更新关键词异常！"
            time.sleep(3)
            continue
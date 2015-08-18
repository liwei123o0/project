# -*- coding: utf-8 -*-
#! /usr/bin/env python
import urllib2
import re
import linecache2
import random
from selenium import webdriver
from mysqlutile import Mysql
import MySQLdb
import time
import sys
reload(sys)
sys.setdefaultencoding('utf8')
#获取关键词写入文件
def keyword(url):
    req =urllib2.Request(url)
    html =urllib2.urlopen(req,timeout=30).read()
    with open("keywords.txt","w")as w:
        w.write(re.sub(r"\r\n",r"\n",html))
#随机获取一个关键词
def readrandom():
    with open("keywords.txt","r")as f:
        count = len(f.readlines())
        num =random.randint(1,count)
        keyword =linecache2.getline("keywords.txt",num)
        return str(keyword)
#mysql获取为爬过关键字
def wordsall():
    conn = MySQLdb.connect(host="10.6.2.121",port=3306,user="root",passwd="root",charset="utf8")
    cur  =conn.cursor()
    cur.execute("SELECT keyword FROM weibo.keyword_fenxi ORDER BY countint LIMIT 1")
    word =cur.fetchall()[0][0]
    cur.execute("UPDATE weibo.keyword_fenxi SET countint = countint+1 WHERE keyword='%s'"%word)
    conn.commit()
    cur.close()
    conn.close()
    return word
def scrapysinaweibo():
        mids =[]
        zfses=[]
        driver =webdriver.Firefox()
        #两种方式一种随机方法readrandom()，一种数据库去为爬过词方法readrandom()
        word = wordsall()
        word = str(word).replace('"',"").replace("+","")
        words =word
        print word
        word = urllib2.quote(word).replace("%0A","")
        driver.get("http://s.weibo.com/weibo/%s"%word)
        driver.implicitly_wait(5)
        # time.sleep(random.randint(5,10))
        #获取所需字段
        midsall  = driver.find_elements_by_xpath("//div[@class='WB_cardwrap S_bg2 clearfix']/div")
        uids     = driver.find_elements_by_xpath("//ul[@class='feed_action_info feed_action_row4']/li[2]/a")
        contens  = driver.find_elements_by_xpath("//div[@class='feed_content wbcon']/p[@class='comment_txt']")
        times    = driver.find_elements_by_xpath("//div[@class='content clearfix']/div[@class='feed_from W_textb']/a[@class='W_textb']")
        zfsesall = driver.find_elements_by_xpath("//ul[@class='feed_action_info feed_action_row4']/li[2]//em")
        usernames = driver.find_elements_by_xpath("//div[@class='feed_content wbcon']/a[@class='W_texta W_fb']")
        userimgs  = driver.find_elements_by_xpath("//div[@class='face']/a/img")
        #评论数有问题
        # plses   = driver.find_elements_by_xpath("//ul[@class='feed_action_info feed_action_row4']/li[3]//em")
        # print "pls:",len(plses)
        #特殊数据处理
        for mid in midsall:
            if mid.get_attribute("mid") ==None:
                continue
            mids.append(mid)
        for zfss in zfsesall:
            zfs= zfss.text
            if zfs ==None:
                zfs ="0"
            elif zfs =="":
                zfs ="0"
            zfses.append(zfs)
        cur =Mysql(host="10.6.2.121")
        cur.conDB()
        for i in range(len(uids)):
            uid= uids[i].get_attribute("action-data")
            uid =re.search(r"(?<=uid=)\d+",uid).group()
            mid = mids[i].get_attribute("mid")
            conten = contens[i].text
            date  = times[i].get_attribute("title")
            zfs = zfses[i]
            username =usernames[i].get_attribute("title")
            userimg = userimgs[i].get_attribute("src")
            group  = "scrapy微博"
            sitename = "新浪微博"
            print username,conten,uid,mid,date,zfs,words,userimg
            # cur.selDB("INSERT INTO weibo.sina(IR_UID,IR_MID,IR_CREATED_AT,IR_STATUS_CONTENT,IR_RTTCOUNT,IR_GROUPNAME,IR_SITENAME,KEYWORD,IR_SCREEN_NAME,IR_PROFILE_IMAGE_URL) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(uid,mid,date,conten,zfs,group,sitename,words,username,userimg))
        driver.quit()
        cur.closeDB()
if __name__=="__main__":
    # keyword("http://10.6.2.124/keywords/keywords.txt")
    # while 1:
    #     try:
    #         scrapysinaweibo()
    #         miao = random.randint(55,90)
    #         print "等待%s秒，开始下个关键词搜索"%miao
    #         time.sleep(miao)
    #     except:
    #         print "程序异常，休息1到3分钟继续"
    #         time.sleep(random.randint(60,180))
    #         continue

    scrapysinaweibo()
    miao = random.randint(55,90)
    print "等待%s秒，开始下个关键词搜索"%miao
    # time.sleep(miao)
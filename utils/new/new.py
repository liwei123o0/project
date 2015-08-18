# -*- coding: utf-8 -*-
#! /usr/bin/env python
import re 
import urllib 
import urllib2 
import MySQLdb 
import time
conn= MySQLdb.connect( 
	host='127.0.0.1',
	port = 3306, 
	user='root',
	passwd='root',
	db ='',
	) 
cur = conn.cursor()
#获取url
def getUrl(urls):
	if urls == '':
		urls = "http://www.yilongnews.com"
	try:
		status=urllib2.urlopen(urls,timeout=15).code
	except:
		status = 203                        #打不开获取不到 状态吗
	if status == 200:
		html = getHtml(urls) 
		cc = getImg(html) 
		cc = list(set(cc)) # qu chongfu 	
		#print cc
		#写入数据库
		for aa in cc: 
			# print aa
			isFind(aa)
	else:
		sql2 = u"update test.get_url set is_geted = '2' where url = '%s'" % (urls)
		cur.execute(sql2)	
		conn.commit()
	return findMin()
	
#数据库中查找最小的 没有爬行过的id ，再次爬行	
def findMin():
	#存入数据库以后，从数据库里面从id最小的开始获取，写入数据库。
	#continue
	print "isfind"
	sql = u"select min(id) from test.get_url where is_geted = 0"
	cur.execute(sql)
	res1 = cur.fetchall()
	urld = res1[0][0]
	print urld
	sql1 = u"select url from test.get_url where id = '%d'" % (urld)
	res = cur.execute(sql1)
	cds=cur.fetchall()	
	again = cds[0][0]
	#把状态改成 1
	sql2 = u"update test.get_url set is_geted = '1' where id = '%d'" % (urld)
	cur.execute(sql2)	
	conn.commit()
	#cur.close() 
	print again
	return	getUrl(again)
#获取网页内容	
def getHtml(url): 
	page = urllib.urlopen(url) 
	html = page.read() 
	return html 

#正则表达式，获取url	
def getImg(html): 
	reg = r'[a-zA-z]+:\/\/www?\.[0-9a-zA-z_]+[\.a-z]+' 
	imgre = re.compile(reg) 
	imglist = re.findall(imgre,html) 
	return imglist 

# 写入数据库
def isFind(aa):
	print aa
	statement = u"select * from test.get_url where url = '%s'" % (aa)
	result = cur.execute(statement)
	conn.commit()
	if result == 0:
		x = u"INSERT INTO test.get_url set url = '%s'" % (aa)
		cur.execute(x)
        # print x
	return
#初始url	
urls = "http://www.yilongnews.com"
#获取url链接	
getUrl(urls)
#findMin()
cur.close() 
conn.commit() 
conn.close()
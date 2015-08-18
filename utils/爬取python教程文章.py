# -*- coding: utf-8 -*-
import urllib2
from lxml import etree
import cookielib
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
class Scrapy(object):
#全局cookie
    def cook(self):
        cooks = cookielib.LWPCookieJar()
        openner = urllib2.build_opener(urllib2.HTTPCookieProcessor(cooks))
        urllib2.install_opener(openner)
#打开python学习网站
    def urlopen(self):
        req = urllib2.Request("http://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000")
        body = urllib2.urlopen(req)
        html = body.read()
#etree解析html
        dom = etree.HTML(html.decode("utf-8"))
        body = dom.xpath("//div[@class='x-wiki-tree']//li/a/@href")
        urllist =[]
        bodylist=[]
        cont =0
        for i in body:
            try:
                cont +=1
                url1 ="http://www.liaoxuefeng.com"+i
                print("正在下载第%s个连接..."%cont)
                print(url1)
                urllist.append(url1)
                print("开始爬取相关页面的内容...")
                req = urllib2.Request(url1)
                body = urllib2.urlopen(req,timeout=30)
                html = body.read()
                dom = etree.HTML(html.decode("utf-8"))
                body = dom.xpath("//div[@class='x-wiki-content x-content']//text()")
                title = dom.xpath("//div[@class='x-wiki-tree']//li/a/text()")
                bodylist.append(body)
                conten1 = "===============%s.%s=================\n"%(cont,"".join(title[cont-1]))
                conten2 = "".join(bodylist[cont-1])
                conten ="".join(conten1+conten2)
                print(conten)
                with open("python.txt",'a')as w:
                    w.write(conten)
            except:
                raw_input("第%s个URL打开失败已跳过此URL连接(按ENTER继续抓取下一页)"%cont)
                continue


while True:
    scrapy = Scrapy()
    # scrapy.cook()
    scrapy.urlopen()
# -*- coding: utf-8 -*-
#! /usr/bin/env python
from  scrapy import Selector,Request
from scrapy.spiders import CrawlSpider,Rule,Spider
from scrapy.linkextractors import LinkExtractor
from spiderweb.items import SpiderbbsItem
from spiderweb.extends.textfile import FileText
import urllib2


import re
import os
import time

from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapy.http import FormRequest

class WeiboSpider(CrawlSpider):
    '''
    这是一个使用scrapy模拟登录新浪微博的例子，
    希望能对广大的同学有点帮助 ，这是所有代码
    '''

    name = 'weibo'
    allowed_domains = ['weibo.com', 'sina.com.cn']

    def start_requests(self):
        username = 'leo.liu@galaxydata.cn'
        url = 'http://login.sina.com.cn/sso/prelogin.php?entry=miniblog&callback=sinaSSOController.preloginCallBack&user=%s&client=ssologin.js(v1.3.14)&_=%s' % \
        (username, str(time.time()).replace('.', ''))
        print url
        return [Request(url=url, method='get', callback=self.post_message)]

    def post_message(self, response):
        serverdata = re.findall('{"retcode":0,"servertime":(.*?),"pcid":"(.*?)","nonce":"(.*?)"}', response.body, re.I)[0]
        print serverdata
        servertime = serverdata[0]
        print servertime
        nonce = serverdata[1]
        print nonce
        formdata = {"entry" : 'miniblog',
        "gateway" : '1',
        "from" : "",
        "savestate" : '7',
        "useticket" : '1',
        "ssosimplelogin" : '1',
        "username" : 'leo.liu@galaxydata.cn',
        "service" : 'miniblog',
        "servertime" : servertime,
        "nonce" : nonce,
        "pwencode" : 'wsse',
        "password" : '080808',
        "encoding" : 'utf-8',
        "url" : 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
        "returntype" : 'META'}

        return [FormRequest(url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.3.14)',
        formdata = formdata,callback=self.check_page) ]

    def check_page(self, response):
        url = 'http://weibo.com/'
        request = response.request.replace(url=url, method='get', callback=self.parse_item)
        return request

    def parse_item(self, response):
        with open('%s%s%s' % (os.getcwd(), os.sep, 'logged.html'), 'wb') as f:
            f.write(response.body)


# class SpiderWEIXIN(Spider):
#     name = "weibo"
#     allowed_domains = []
#     # download_delay = 0.5
#     start_urls = []
#     for i in xrange(4):
#         word = FileText.loadkeyword()
#         wordurl = urllib2.quote(word)
#         url = "http://www.baidu.com/s?tn=baiduwb&rtt=2&cl=2&rn=50&ie=utf-8&bs=%E8%A5%BF%E5%AE%89123&f=8&rsv_bp=1&wd={}".format(wordurl)
#         start_urls.append(url)
#     #不同页面之间传值
#     def parse(self, response):
#         item = SpiderbbsItem()
#         sel = Selector(text=response.body)
#         item['IR_URLNAME2'] = response.url
#         item['IR_KEYWORD']  = self.word
#         for i in sel.xpath("//div[@class='weibo_detail']"):
#             item['IR_URLNAME'] = "".join(i.xpath(".//div[@class='m']/a[1]/@href").extract())
#             #页面传值
#             item['IR_URLNAME2']  = response.url
#             item['IR_URLTITLE'] = "".join(sel.xpath("./p[1]//text()").extract())
#             item['IR_URLTIME']  = "".join(sel.xpath("//em[@id='post-date']/text()").extract())
#             item['IR_SRCNAME']  = "".join(sel.xpath("./p[1]/a[1]/text()").extract())
#             item['IR_CONTENT']  = "".join(sel.xpath("./p[1]//text()").extract())
#             yield item
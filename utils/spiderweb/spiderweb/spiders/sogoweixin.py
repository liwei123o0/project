# -*- coding: utf-8 -*-
#! /usr/bin/env python
from  scrapy import Selector,Request
from scrapy.spiders import CrawlSpider,Rule,Spider
from scrapy.linkextractors import LinkExtractor
from spiderweb.items import SpiderbbsItem
from spiderweb.extends.textfile import FileText
import urllib2

class SpiderWEIXIN(Spider):
    name = "weixin"
    allowed_domains = []
    # download_delay = 0.5
    start_urls = []
    for i in xrange(40):
        word = FileText.loadkeyword()
        wordurl = urllib2.quote(word)
        url = "http://weixin.sogou.com/weixin?type=2&query={}&fr=sgsearch&ie=utf8&_ast=1438839680&_asf=null&w=01019900&cid=null&sut=855&sst0=1438839884029&lkt=0%2C0%2C0".format(wordurl)
        start_urls.append(url)
    #不同页面之间传值
    def parse(self, response):
        item = SpiderbbsItem()
        sel = Selector(text=response.body)
        item['IR_URLNAME2'] = response.url
        item['IR_KEYWORD']  = "".join(sel.xpath("//input[@id='upquery']/@value").extract())
        urls = sel.xpath("//h4")
        for i in urls:
            url = "".join(i.xpath("./a/@href").extract())
            #页面传值
            request = Request(url,callback=self.parse_item)
            request.meta['item'] = item
            yield request

    def parse_item(self, response):
        sel = Selector(text=response.body)
        item = response.meta['item']
        item['IR_URLNAME']  = response.url
        item['IR_URLTITLE'] = "".join(sel.xpath("(//h2)[1]/text()").extract())
        item['IR_URLTIME']  = "".join(sel.xpath("//em[@id='post-date']/text()").extract())
        item['IR_SRCNAME']  = "".join(sel.xpath("//a[@id='post-user']/text()").extract())
        item['IR_CONTENT']  = "".join(sel.xpath("//div[@id='js_content']//text()").extract())
        yield item
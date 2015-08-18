# -*- coding: utf-8 -*-
#! /usr/bin/env python
from  scrapy import Selector
from scrapy.spiders import Spider
from spiderweb.items import SpiderbbsItem
from spiderweb.extends.textfile import FileText
import urllib2

class SpiderBBS(Spider):
    name = "bbs"
    allowed_domains = []
    # download_delay = 0.5
    start_urls = []
    for i in xrange(4):
        word = FileText.loadkeyword()
        wordurl = urllib2.quote(word)
        url = "http://www.sogou.com/web?query={}&ie=utf8&_ast=1438758528&_asf=null&w=01029901&p=40040100&dp=1&cid=&cid=&interation=196648&sut=8584&sst0=1438758432575&lkt=2%2C1438758430663%2C1438758430894".format(wordurl)
        start_urls.append(url)

    def parse(self, response):
        sel = Selector(response)
        item = SpiderbbsItem()
        item['IR_KEYWORD']  = "".join(sel.xpath("//input[@id='upquery']/@value").extract())
        for i in sel.xpath("//div[@class='rb']"):
            item['IR_URLNAME2'] = response.url
            item['IR_URLNAME']  = "".join(i.xpath("./h3/a/@href").extract())
            item['IR_URLTITLE'] = "".join(i.xpath("./h3/a//text()").extract())
            item['IR_URLTIME']  = "".join(i.xpath("./div[@class='fb']/cite/text()").extract())
            item['IR_SRCNAME']  = "".join(i.xpath("./div[@class='fb']/cite/text()").extract())
            item['IR_CONTENT']  = "".join(i.xpath("./div[@class='ft']//text()").extract())
            yield item
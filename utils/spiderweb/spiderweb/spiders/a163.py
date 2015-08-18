# -*- coding: utf-8 -*-
from  scrapy import Selector
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from spiderweb.items import SpiderwebItem
from spiderweb.extends.textfile import FileText
import logging
class Spider163(CrawlSpider):

    name = "huhu"

    def __init__(self,config):

        self.load_config(config)

        return super(Spider163, self).__init__()

    def load_config(self,config_path):

        txt = FileText.load_config(config_path)

        logging.log(logging.WARNING,txt)

        self.allowed_domains = []
        self.start_urls = [
            "http://10.6.2.124:8080/",
        ]
        self.rules = [
            # 提取匹配 huhuuu/default.html\?page\=([\w]+) 的链接并跟进链接(没有callback意味着follow默认为True)
            Rule(LinkExtractor(restrict_xpaths="//h2/a[3]"),
                    ),
            Rule(LinkExtractor(restrict_xpaths="//tr[@class='even'][2]/td/a"),
                    ),
            # 提取匹配 'huhuuu/p/' 的链接并使用spider的parse_item方法进行分析
            Rule(LinkExtractor(restrict_xpaths="//td/a",),
                callback='parse_item',
            )
        ]


    def parse_item(self, response):
        sel = Selector(response)
        item = SpiderwebItem()
        item['conten'] = sel.xpath('//body//text()').extract()[0]
        item['title'] = response.url

        yield item
# -*- coding: utf-8 -*-
from scrapy.spider import Spider,CrawlSpider
from scrapy.selector import Selector
from confcrawl.utils import utils
from confcrawl.items import ConfcrawlItem

class ExampleSpider(Spider):

    name = "example"
    allowed_domains = ["douban.com"]

    def __init__(self,path=None):

        self.load_config(path)

        return  super(ExampleSpider,self).__init__()

    def load_config(self,path):

        ut = utils.utilsconfig()
        conf = ut.read_config(path)

        # self.allowed_domains = conf.get('domains',[])
        self.start_urls = conf.get("start_urls",[])

    def parse(self, response):
        item = ConfcrawlItem()
        sel = Selector(response)
        title = "".join(sel.xpath("//title/text()").extract()[0])
        item["title"] = title
        return item
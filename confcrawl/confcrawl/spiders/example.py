# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
import json

class ExampleSpider(scrapy.Spider):

    name = "example"

    def __init__(self):
        self.load_config()
        return  super(ExampleSpider,self).__init__()

    def load_config(self):

        with open("E:\projectall\project\confcrawl\confcrawl\config\example.conf","r")as f:
            config = f.read()
        conf = json.loads(config)
        self.allowed_domains = conf.get("allowed_domains",[])
        self.start_urls = ["http://www.360doc.com/content/11/1011/14/7472437_155166461.shtml"]


    def parse(self, response):
        sel = Selector(response)
        title = sel.xpath("//title/text()").extract()[0]
        print title

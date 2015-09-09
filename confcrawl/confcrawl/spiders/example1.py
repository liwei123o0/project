# -*- coding: utf-8 -*-
import bs4

from scrapy.selector import Selector
from scrapy.spider import Spider,Request
from confcrawl.items import DoubanBookItem

class DoubanBookSpider(Spider):
    name = "doubanBook"
    allowed_domains = ["douban.com"]
    start_urls = [
        "http://book.douban.com",
    ]
    def parse(self, response):
        """通过 xpath 获取热门电子书的链接"""
        sel = Selector(response)
        sites = sel.xpath('//div[@class="section ebook-area"]//ul[@class="list-col list-col5"]/li//div[@class="title"]')
        for site in sites:
            title = site.xpath('a/@title').extract()
            link = site.xpath('a/@href').extract()
            title, link = title[0], link[0]
            # print title, link
            yield Request(url=link, callback=self.parse2)
    def parse2(self, response):
        """
        解析电子书详细信息页面，使用 dom 解析获取数据
        """
        soup = bs4.BeautifulSoup(response.body)
        bookInfo = soup.findAll('div', attrs={'class':'article-profile-bd'})
        if bookInfo:
            bookInfo = bookInfo[0]
            item = DoubanBookItem()
            item['title'] = "".join(bookInfo.findAll('h1', attrs={'class':'article-title'})[0].strings)
            item['author'] = "".join(bookInfo.findAll('p', attrs={'class':'author'})[0].strings)
            item['category'] = "".join(bookInfo.findAll('p', attrs={'class':'category'})[0].strings)
            # item['price'] = bookInfo.findAll('div', attrs={'class':'article-actions purchase-none purchase-layout-horizontal'})[0]['data-readable-price']
            # debug
            return item
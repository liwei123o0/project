# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field

class ConfcrawlItem(Item):
    # define the fields for your item here like:
    title = Field()



class DoubanBookItem(Item):
    title = Field()
    author = Field()
    publisher = Field()
    category = Field()
    price = Field()
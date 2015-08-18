# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
from scrapy import Item,Field

class SpiderwebItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    conten = Field()
    title = Field()

class SpiderbbsItem(Item):
    IR_URLTITLE = Field()
    IR_SRCNAME = Field()
    IR_CONTENT = Field()
    IR_URLTIME = Field()
    IR_URLNAME = Field()
    IR_KEYWORD = Field()
    IR_URLNAME2 = Field()

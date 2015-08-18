# -*- coding: utf-8 -*-
#! /usr/bin/env python
from scrapy import cmdline
import re
# cmdline.execute("scrapy crawl huhu -a config=E:\project\spiderweb\spiderweb\items.py".split())
cmdline.execute("scrapy crawl weibo".split())
# a = '''
#                         【贯彻全会精神】适应新常态  坚持总基调
#                         '''
# print re.sub(r"\s+","",a)
# print re.findall(r'\d{4}.*',a)[0]
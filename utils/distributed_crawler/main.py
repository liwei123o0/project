# -*- coding: utf-8 -*-
#! /usr/bin/env python

from scrapy import cmdline
# cmdline.execute("scrapy crawl test -a config=http://10.6.2.124/conf/yuqing/huxiwang.conf -a debug=true".split())
cmdline.execute("scrapy crawl test -a config=E:\project\distributed_crawler\huxiwang.conf -a debug=true".split())
# cmdline.execute("scrapy crawl test -a config=http://10.6.2.124/conf/yuqing/blogchina.conf".split())

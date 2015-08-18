# -*- coding: utf-8 -*-
#! /usr/bin/env python

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
from datetime import datetime
import logging
import traceback
from distributed_crawler.utilses import utils
from scrapy.conf import settings
import pymongo

def item2post(item):
    post = {}
    for k,v in item.fields.iteritems():
        if 'name' in v:
            post[v['name']] = item[k]
    return post


class DistributedCrawlerPipeline(object):
    def process_item(self, item, spider):
        return item

class DebugPipeline(object):
    def open_spider(self, spider):
        self.idx = 0

    def process_item(self, item, spider):
        if not (hasattr(spider, 'debug') and spider.debug):
            for k,v in item.iteritems():
                try:
                    updataitem = {k:v[0]}
                    item.update(updataitem)
                except:
                    pass
            return item

        self.idx += 1
        print '{:=^60}'.format(self.idx)
        for k,v in item.iteritems():
            v = v[0]
            if type(v) in [str, unicode]:
                v = re.sub(r'\s{2,}', ' ', v.replace('\n', ' ').replace('\r', ''))
                if spider.verbose<3 and len(v)>74:
                    v = u'{} {} {}'.format(v[:60].strip(), u'...', v[-14:].strip())
            f = ' ' if 'name' in item.fields[k] else '*'
            print u'{:>15.15}{}: {}'.format(k, f, v)
        return item

###MySQL入库方式###
class MysqlPipeline(object):
    def open_spider(self, spider):
        if hasattr(spider, 'mysql'):
            try:
                uri = spider.mysql
                self.cnn, _, self.tbl = utils.connect_uri(uri)
                self.cur = self.cnn.cursor()
                logging.info(u'mysql：<{}> 连接成功！'.format(uri))
                return
            except Exception as ex:
                traceback.print_exc()
                logging.error(u'mysql: {} 连接失败！'.format(ex))

        self.cnn = self.cur = None

    def process_item(self, item, spider):
        if self.cnn:
            try:
                post = item2post(item)
                fields = []
                values = []
                for k,v in post.iteritems():
                    fields.append(k)
                    values.append(v)
                self.cur.execute("""INSERT INTO {}({}) VALUES({});""".format(
                                                                                self.tbl,
                                                                                ','.join(fields),
                                                                                ','.join(['%s']*len(fields))
                                                                            ), values)
                self.cnn.commit()
            except Exception as ex:
                traceback.print_exc()
        return item

    def close_spider(self, spider):
        if self.cnn:
            logging.info(u'mysql已经断开')
            self.cur.close()
            self.cnn.close()
            self.cnn = self.cur = None
###MongoDB入库方式###
class MongoPipeline(object):
    def __init__(self):
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        dbName = settings['MONGODB_DBNAME']
        client = pymongo.MongoClient(host=host, port=port)
        tdb = client[dbName]
        self.post = tdb[settings['MONGODB_DOCNAME']]

    def process_item(self, item, spider):
        if not (hasattr(spider, 'debug') and spider.debug):
            for k,v in item.iteritems():
                updataitem = {k:v[0]}
                item.update(updataitem)
            bookInfo = dict(item)
            self.post.insert(bookInfo)
        return item
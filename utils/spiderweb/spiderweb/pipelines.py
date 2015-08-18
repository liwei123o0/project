# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import re
class SpiderwebPipeline(object):
    def open_spider(self, spider):
        self.idx = 0
        self.conn = MySQLdb.connect(host="10.6.2.121",user="root",passwd="root",port=3306,charset="utf8")
        self.cur = self.conn.cursor()

    def process_item(self, item, spider):
        try:
            item['IR_URLTIME'] = re.sub(r"\s+","",item['IR_URLTIME'])
            item['IR_CONTENT'] = re.sub(r"\s+","",item['IR_CONTENT'])
        except:
            print "error"
        print "==============%s=================="%self.idx
        print "IR_URLTITLE:"+item['IR_URLTITLE']
        print "IR_CONTENT:"+item['IR_CONTENT']
        print "IR_SRCNAME:"+item['IR_SRCNAME']
        print "IR_URLTIME:"+item['IR_URLTIME']
        print "IR_URLNAME:"+item['IR_URLNAME']
        print "IR_KEYWORD:"+item['IR_KEYWORD']
        print "IR_URLNAME2:"+item['IR_URLNAME2']
        self.idx+=1
        try:
            self.cur.execute("INSERT INTO zjfx.news_weixin(IR_URLTITLE,IR_CONTENT,IR_SRCNAME,IR_URLTIME,IR_URLNAME,IR_KEYWORD,IR_URLNAME2) VALUES ('%s','%s','%s','%s','%s','%s','%s')"%(item['IR_URLTITLE'],item['IR_CONTENT'],item['IR_SRCNAME'],item['IR_URLTIME'],item['IR_URLNAME'],item['IR_KEYWORD'],item['IR_URLNAME2']))
            self.conn.commit()
        except MySQLdb.Error,e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return item
    def close_spider(self, spider):
        if self.conn:
            self.cur.close()
            self.conn.close()

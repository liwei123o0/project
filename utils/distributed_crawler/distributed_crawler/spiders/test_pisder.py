# -*- coding: utf-8 -*-
#! /usr/bin/env python

import logging
import json
import traceback
import re
from scrapy.spiders import CrawlSpider,Rule
from scrapy.exceptions import CloseSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.item import Item, Field
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
# from distributed_crawler import settings
from scrapy_redis.spiders import RedisSpider

from distributed_crawler.utilses import utils


class MySpider(CrawlSpider):
    name = 'test'
    def __init__(self,config=None,verbose=0, **kwargs):
        '''
        :param config:爬虫配置文件路径
        :param verbose:详细行数
        :param kwargs:
        :return:调用父类的__init__()方法
        '''
        self.load_config(config)
        self.verbose = int(verbose)
        self.tz = kwargs.get('tz', '+00:00')
        if kwargs.get('debug')!=None:
            self.debug = str(kwargs.get('debug', False)).upper()=='TRUE'

            if self.debug:
                logging.info(u'{:=^20}'.format(' DEBUG MODE '))

                if hasattr(self, 'mysql'):
                    logging.log(logging.WARNING,u'disable mysql')
                    del self.mysql

        return super(MySpider,self).__init__()

    def load_config(self, config_path):
        '''
        :param config_path: 配置文件路径参数
        :return:错误返回值
        '''
        txt = utils.load_file(config_path)
        if not txt:
            logging.log(logging.INFO,u"错误：%s----配置文件路径不存在！"%config_path)
            raise CloseSpider()
        #打印配置文件详情
        print txt
        conf = json.loads(txt)
        #### site###
        self.site = conf.get('site', u'未知站点')
        self.macro = utils.MacroExpander({
            'SITE': self.site,
            'CONF': json.dumps(conf)
        })

        ###爬虫域名设置###
        self.allowed_domains = conf.get('domains', [])

        ####爬虫入口start_urls###
        urls =conf.get('urls',[])
        self.start_urls = utils.generate_urls(urls,self.macro)

        #### debug
        self.debug = conf.get('debug', False)

        #### rules
        self.rules = []
        self.page_extractor = None

        for k,v in conf.get('rules',{}).iteritems():
            ###给多个rules规则赋值###
            follow = v.get('follow', True)
            callback = None if follow else 'parse_page'
            regex = self.macro.expand(v.get('regex'))
            xpath = self.macro.expand(v.get('xpath'))
            pages = v.get('pages')
            sub = v.get('sub')
            rule = Rule(
                LinkExtractor(
                    allow=regex,
                    restrict_xpaths=xpath,
                    process_value=utils.first_n_pages(regex, pages)),
                process_links=self.sub_links(sub),
                callback=callback,
                follow=follow
            )
            self.rules.append(rule)
        if not self.rules:
            self.parse = self.parse_page
            self.make_page_extractor(conf.get('urls', []))

        ### mappings(loop/fields)
        self.build_mappings(conf)

        ### database
        for db in ['mongodb', 'mysql']:
            if db in conf:
                setattr(self, db, conf[db])

        ###添加插件plugin###
        if hasattr(self, 'plugin'):
            self.plugin = utils.load_plugin(self.plugin)
            self.plugin.spider = self
        else:
            self.plugin = None

        ### settings###
        for k,v in conf.get('settings', {}).iteritems():
            logging.info(u'+SET {} = {}'.format(k, v))
            setattr(self, k, v)

    def build_mappings(self, conf, lvl=0):
        if lvl==0:
            self.mappings = dict()
            for k,v in conf['fields'].iteritems():
                Item.fields[k] = Field()
                if 'name' in v:
                    Item.fields[k]['name'] = v['name']

        self.mappings[lvl] = {
            'loop': conf.get('loop'),
            'fields': conf.get('fields')
        }

        if 'continue' in conf:
            self.build_mappings(conf.get('continue'), lvl+1)

    def run_plugin(self, response):
        if response.meta.get('dirty')==False:
            return response.replace(url=response.meta.get('url', response.url))
        elif self.plugin:
            output = self.plugin.parse(
                url=response.url,
                body=response.body,
                meta=response.meta,
                status=response.status,
                headers=response.headers
            )
            if isinstance(output, Request):
                output.meta['dirty'] = False
                return output.replace(callback=self.parse_page)
            else:
                return response.replace(body=output)
        else:
            return response

    ###替换函数###
    def sub_links(self, sub):
        if not sub:
            return None

        frm = sub.get('from')
        to = sub.get('to')

        def _sub(links):
            new_links = []
            for i in links:
                i.url = re.sub(frm, to, i.url)
                new_links.append(i)
            return new_links

        return _sub

    def maybe_continue(self, item, response):
        meta = response.meta
        item = self.update_item(meta.get('item', Item()), item)
        lvl = meta.get('level', 0)
        mapping = self.mappings[lvl]
        fields = mapping['fields']
        for k,v in fields.iteritems():
            ps = v.get('parse', [{}])
            if not isinstance(ps, list):
                ps = [ps]
            if ps[-1].get('type')=='continue':
                url = item[k][0]
                meta = {
                    'level':lvl+1,
                    'item':item
                }
                return Request(url, meta=meta, callback=self.parse_page, dont_filter=True)
        return item

    def update_item(self, origin, patch):
        for k,v in patch.fields.iteritems():
            if k in patch:
                origin[k] = patch[k]
        return origin

    def parse_page(self, response):
        try:
            response = self.run_plugin(response)
            if isinstance(response, Request):
                yield response
                return

            lvl = response.meta.get('level', 0)
            mapping = self.mappings[lvl]
            loop, fields = mapping['loop'], mapping['fields']

            for item in self.parse_item(response, loop, fields):
                yield self.maybe_continue(item, response)

            if self.page_extractor:
                for link in self.page_extractor.extract_links(response):
                    yield Request(link.url, meta=response.meta)

        except Exception as ex:
            logging.log(logging.INFO,u'%s\n%s'%(response.url, traceback.format_exc()))

    def make_page_extractor(self, obj):
        if type(obj)!=dict:
            return
        pages = obj.get('pages')
        if pages:
            regex = self.macro.expand(pages.get('regex'))
            xpath = self.macro.expand(pages.get('xpath'))
            self.page_extractor = LinkExtractor(
                                        allow=regex,
                                        restrict_xpaths=xpath,
                                        process_value=utils.first_n_pages(regex, pages))

    def parse_item(self, response, loop, fields):
        hxs = Selector(response)
        self.macro.update({'URL':response.url})

        for e in hxs.xpath(loop or '(//*)[1]'):
            loader = ItemLoader(item=Item(), selector=e)

            for k,v in fields.iteritems():
                if 'value' in v:
                    get_v_x = loader.get_value
                    v_x = v.get('value')
                elif 'xpath' in v:
                    get_v_x = loader.get_xpath
                    v_x = v.get('xpath')
                else:
                    logging.log(logging.WARNING,u'field [%s] should contains "value" or "xpath"'%(k))
                    continue

                val = get_v_x(
                    self.macro.expand(v_x),
                    utils.convert_type(v.get('parse', {})),
                    re=v.get('regex')
                )

                if not val and 'default' in v:
                    val = self.macro.expand(v.get('default'))

                qry = v.get('filter', {})
                if utils.filter_data(qry, val):
                    loader.add_value(k, val)
                else:
                    break
            else:
                yield loader.load_item()
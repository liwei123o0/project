#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# A complicated spider written by Kev++
# 2013-09-02

from urllib2 import urlparse
import re
import json
import Cookie
import traceback

from scrapy import log
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.exceptions import CloseSpider
from scrapy.http import Request, FormRequest
from scrapy.item import Item, Field
from scrapy.selector import HtmlXPathSelector
from scrapy.utils.misc import arg_to_iter
from scrapy.utils.datatypes import CaselessDict

from example.utils import utils
from example import settings
import jsonpath


class ExampleSpider(CrawlSpider):

    name = 'example'

    def __init__(self, config=None, verbose=0, **kwargs):
        utils.help()
        self.load_config(config)
        self.verbose = int(verbose)
        self.tz = kwargs.get('tz', '+00:00')
        if kwargs.get('debug')!=None:
            self.debug = str(kwargs.get('debug', False)).upper()=='TRUE'
            if self.debug:
                log.msg(utils.G(u'{:=^20}'.format(' DEBUG MODE ')))
                if hasattr(self, 'mongo'):
                    log.msg(utils.Y(u'disable mongo'), level=log.WARNING)
                    del self.mongo
                if hasattr(self, 'mysql'):
                    log.msg(utils.Y('disable mysql'), level=log.WARNING)
                    del self.mysql
                if hasattr(self, 'zmq'):
                    log.msg(utils.Y(u'disable zmq'), level=log.WARNING)
                    del self.zmq
        return super(ExampleSpider, self).__init__()

    def load_config(self, config_path):
        txt = utils.load_file(config_path)
        if not txt:
            raise CloseSpider()

        conf = json.loads(txt)
        log.msg(u'loading config from <{}>:\n{}'.format(unicode(config_path, encoding='utf-8'),
                json.dumps(conf, indent=4, ensure_ascii=False, sort_keys=True)))

        #### config
        self.config = config_path

        #### debug
        self.debug = conf.get('debug', False)

        #### site
        self.site = conf.get('site', u'未知站点')
        self.macro = utils.MacroExpander({
            'SITE': self.site,
            'CONF': json.dumps(conf)
        })

        #### allowed_domains
        self.allowed_domains = conf.get('domains', [])

        #### start_urls
        urls = conf.get('urls', [])
        self.start_urls = utils.generate_urls(urls, self.macro)
        self.start_method = urls.get('method', 'GET') if type(urls)==dict else 'GET'
        self.make_headers(urls.get('headers', {}) if type(urls)==dict else {})

        #### rules
        self.rules = []
        self.page_extractor = None
        for k,v in conf.get('rules', {}).iteritems():

            follow = v.get('follow', True)
            callback = None if follow else 'parse_page'
            regex = self.macro.expand(v.get('regex'))
            xpath = self.macro.expand(v.get('xpath'))
            pages = v.get('pages')
            sub = v.get('sub')

            rule = Rule(
                SgmlLinkExtractor(
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

        ### proxy
        self.proxy = conf.get('proxy', {})

        ### database
        for db in ['mongo', 'mysql', 'zmq']:
            if db in conf:
                setattr(self, db, conf[db])

        ### settings
        # self.logger = settings.DEFAULT_LOGGER
        self.dedup = settings.DEFAULT_DEDUP
        for k,v in conf.get('settings', {}).iteritems():
            log.msg(utils.G('+SET {} = {}'.format(k, v)))
            setattr(self, k, v)

        ### plugin
        if hasattr(self, 'plugin'):
            self.plugin = utils.load_plugin(self.plugin)
            self.plugin.spider = self
        else:
            self.plugin = None

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

    def make_requests_from_url(self, url):
        us = urlparse.urlsplit(url)
        qstr = dict(urlparse.parse_qsl(us.query))
        base = urlparse.urlunsplit(us._replace(query=''))
        return FormRequest(base, formdata=qstr, method=self.start_method, headers=self.headers, cookies=self.cookies, dont_filter=True)

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
            log.msg(u'{}\n{}'.format(response.url, traceback.format_exc()))

    def parse_item(self, response, loop, fields):
        hxs = HtmlXPathSelector(response)
        self.macro.update({'URL':response.url})

        for e in hxs.select(loop or '(//*)[1]'):
            loader = XPathItemLoader(item=Item(), selector=e)

            for k,v in fields.iteritems():
                if 'value' in v:
                    get_v_x = loader.get_value
                    v_x = v.get('value')
                elif 'xpath' in v:
                    get_v_x = loader.get_xpath
                    v_x = v.get('xpath')
                else:
                    log.msg(u'field [{}] should contains "value" or "xpath"'.format(k), level=log.WARNING)
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

    def make_headers(self, headers):
        headers = CaselessDict(headers)
        if 'user-agent' in headers:
            self.user_agent = headers.pop('user-agent')
        self.cookies = self.make_cookies(headers.pop('cookies', {}))
        self.headers = headers

    def make_cookies(self, cookies):
        if type(cookies) == unicode:
            cookies = cookies.encode('utf-8')
        if type(cookies)==str:
            cookies = {i.key:i.value for i in Cookie.SimpleCookie(cookies).values()}
        elif type(cookies)==dict:
            cookies = cookies
        else:
            cookies = {}
        return cookies

    def make_page_extractor(self, obj):
        if type(obj)!=dict:
            return
        pages = obj.get('pages')
        if pages:
            regex = self.macro.expand(pages.get('regex'))
            xpath = self.macro.expand(pages.get('xpath'))
            self.page_extractor = SgmlLinkExtractor(
                                        allow=regex,
                                        restrict_xpaths=xpath,
                                        process_value=utils.first_n_pages(regex, pages))


class JsonbotSpider(ExampleSpider):
    name = "jsonbot"

    def parse_item(self, response, loop, fields):
        try:
            txt = utils.to_unicode(response.body)
            if hasattr(self, 'json_type') and self.json_type=='list':
                l, r = txt.find('['), txt.rfind(']')
            else:
                l, r = txt.find('{'), txt.rfind('}')
            obj = json.loads(txt[l:r+1])
            self.macro.update({'URL':response.url})

            for e in jsonpath.jsonpath(obj, loop or '$[]') or []:
                item = Item()

                for k,v in fields.iteritems():
                    if 'value' in v:
                        v_x = v.get('value')
                    elif 'jpath' in v:
                        v_x = jsonpath.jsonpath(e, self.macro.expand(v.get('jpath')))
                    else:
                        log.msg(u'field [{}] should contains "value" or "jpath"'.format(k), level=log.WARNING)
                        continue

                    val = utils.convert_type(v.get('parse', {}))(self.macro.expand(v_x))

                    if not val and 'default' in v:
                        val = self.macro.expand(v.get('default'))

                    qry = v.get('filter', {})
                    if utils.filter_data(qry, val):
                        item[k] = arg_to_iter(val)
                    else:
                        break
                else:
                    yield item

        except Exception as ex:
            log.msg(u'{}\n{}'.format(response.url, traceback.format_exc()))
# -*- coding: utf-8 -*-
#! /usr/bin/env python
import os
from urllib2 import urlopen
import urlparse
import platform
import logging
import string
from datetime import datetime,timedelta
import time
import re
import base64
import json
from urllib2 import quote
import jsonpath
from HTMLParser import HTMLParser
from lxml.html.clean import Cleaner
from chardet import detect
from scrapy.exceptions import CloseSpider
from scrapy.utils.markup import remove_tags
from scrapy.loader.processors import Compose,Join,TakeFirst


###判别操作系统加载正确文件路径返回文件###

def load_file(path):
    if os.path.exists(path):
        path = os.path.abspath(path)
        if platform.system() =='Windows':
            path =path.replace('\\','/')
            path = 'file:///'+path
        else:
            path = 'file://'+path
    try:
        txt = urlopen(path, timeout=10).read()
        txt = to_unicode(txt)
    except Exception as ex:
        txt = u''
    return txt
###将编码转换为unicode码###
def to_unicode(txt):
    if type(txt)==unicode:
        return txt
    elif type(txt)==str:
        enc = 'gbk' if detect(txt[:2048])['encoding'].lower()=='gb2312' else 'utf-8'
        return txt.decode(enc)
    else:
        return u''
def generate_urls(obj, macro):
    try:
        if type(obj)==list:
            for url in obj:
                yield macro.expand(url)
        elif type(obj)==dict:
            base = macro.expand(obj['base'].encode('utf-8'))
            us = urlparse.urlsplit(base)
            qstr = dict(urlparse.parse_qsl(us.query))
            qstr.update(obj.get('qstr', {}))
            base = urlparse.urlunsplit(us._replace(query=''))

            for k,v in qstr.iteritems():
                if type(v)==dict and type(v['val'])==unicode:
                    v = v['val'].encode(v.get('enc', 'utf-8'), errors='ignore')
                qstr[k] = macro.expand(v)

            if 'keywords' in obj:
                kw_obj = obj['keywords']
                for kw in load_keywords(kw_obj):
                    key = kw_obj['name'].encode('utf-8')
                    val = kw.encode(kw_obj.get('enc', 'utf-8'), errors='ignore') if type(kw)==unicode else str(kw)
                    if kw_obj.get('query', True):
                        qstr.update({key:val})
                        url = base+'?'+quote(qstr)
                    else:
                        url = base.replace(key, val)+'?'+quote(qstr)
                    yield url
            else:
                url = base+'?'+quote(qstr)
                yield url
    except Exception as ex:
        logging.log(logging.ERROR,u'cannot generate urls: %s'%ex)
        raise CloseSpider()

def load_keywords(kw_obj, msg='keywords'):
    keywords = set()

    if type(kw_obj)==dict:
        path = kw_obj.get('file')

        if path:
            for line in load_file(kw_obj['file']).splitlines():
                kw = line.strip()
                if kw and not kw.startswith('#'):
                    keywords.add(kw)

        for kw in kw_obj.get('list', []):
            keywords.add(kw)

        sub = kw_obj.get('sub')

        if sub:
            frm = sub.get('from')
            to = sub.get('to')
            keywords = {re.sub(frm, to, kw) for kw in keywords}

        logging.warning(u'load {} from <{}>({})'.format(msg, path, len(keywords)))

    return keywords

class MacroExpander(object):

    def __init__(self, env):
        self.macros = dict()
        self.macros.update(env)

    def update(self, env={}):
        now = datetime.now().replace(microsecond=0)
        utcnow = datetime.utcnow().replace(microsecond=0)
        ###时间类型字典###
        self.macros.update({
                'UTCNOW':   utcnow.strftime('%Y-%m-%d %H:%M:%S'),
                'NOW':      now.strftime('%Y-%m-%d %H:%M:%S'),
                'TODAY':    now.strftime('%Y-%m-%d'),
                'ITODAY':   '{}-{}-{}'.format(now.year, now.month, now.day),

                'YEAR':     now.strftime('%Y'),
                'MONTH':    now.strftime('%m'),
                'DAY':      now.strftime('%d'),
                'HOUR':     now.strftime('%H'),
                'MINUTE':   now.strftime('%M'),
                'SECOND':   now.strftime('%S'),

                'IYEAR':    str(now.year),
                'IMONTH':   str(now.month),
                'IDAY':     str(now.day),
                'IHOUR':    str(now.hour),
                'IMINUTE':  str(now.minute),
                'ISECOND':  str(now.second),

                'UNOW':     str(int(time.time())),
                'UTODAY':   str(int(time.mktime(time.strptime(now.strftime('%Y-%m-%d'), '%Y-%m-%d')))),
                'UENDDAY':  str(int(time.mktime(time.strptime(now.strftime('%Y-%m-%d 23:59:59'), '%Y-%m-%d %H:%M:%S'))))
        })

        self.macros.update(env)

    def expand(self, value):
        if type(value)!=str and type(value)!=unicode:
            return value
        template = string.Template(value)
        self.update()
        return template.safe_substitute(self.macros)
###翻页功能###
def first_n_pages(pattern, pages):
    if not pages:
        return None

    start = pages.get('start', 1)
    stop = pages.get('stop', 5)
    group = pages.get('group', 1)
    enc = pages.get('enc')

    def _filter(url):
        m = re.search(pattern, url)
        if m and start<=int(m.group(group))<stop:
            if enc:
                return urlparse.unquote(url).decode('utf-8').encode(enc)
            else:
                return url
        return None

    return _filter
###类型转换###
def convert_type(infs):
    def _wrapper(inf, t):
        def _convert(data):
            if t not in ['join', 'list'] and isinstance(data, list):
                data = TakeFirst()(data)
                if type(data) in [str, unicode]:
                    data = data.strip()
                elif type(data) in [int, float, datetime]:
                    data = str(data)
                else:
                    return data

            if t=='join':
                sep = inf.get('sep', u' ')
                return Join(sep)(data)
            elif t=='list':
                sep = inf.get('sep', u' ')
                return remove_tags(Join(sep)(data)).strip()
            elif t=='text':
                return remove_tags(data).strip()
            elif t=='clean':
                cleaner = Cleaner(style=True, scripts=True, javascript=True, links=True, meta=True)
                return cleaner.clean_html(data)
            elif t=='unesc':
                return HTMLParser().unescape(data)
            elif t=='base64':
                return base64.decodestring(data)
            elif t=='sub':
                frm = inf.get('from')
                to = inf.get('to')
                return re.sub(frm, to, data)
            elif t=='jpath':
                qs = inf.get('query')
                return jsonpath.jsonpath(json.loads(data), qs)
            elif t=='map':
                m = inf.get('map')
                d = inf.get('default')
                return m.get(data, d)
            elif t=='int':
                return int(float(data))
            elif t=='float':
                return float(data)
            elif t=='date':
                fmt = inf.get('fmt', 'auto')
                tz = inf.get('tz', '+00:00')
                return parse_date(data, fmt, tz)
            elif t=='cst':
                fmt = inf.get('fmt', 'auto')
                return parse_date(data, fmt, '+08:00')
            else:
                return data
        return _convert

    infs = infs if type(infs)==list else [infs]
    return Compose(*[_wrapper(inf, inf.get('type', 'str')) for inf in infs])
###时间处理###
def parse_date(data, fmt, tz):
    offset = tz_offset(tz)

    if fmt=='auto':
        now = datetime.utcnow().replace(microsecond=0)+offset
        now_1 = now-timedelta(days=1)
        now_2 = now-timedelta(days=2)

        # 几/刚/今天/昨天/前天
        x = data.strip()
        x = x.replace(u'几', ' 0 ')
        x = x.replace(u'刚[刚才]', now.strftime(' %Y-%m-%d %H:%M:%S '))
        x = x.replace(u'今天', now.strftime(' %Y-%m-%d '))
        x = x.replace(u'昨天', now_1.strftime(' %Y-%m-%d '))
        x = x.replace(u'前天', now_2.strftime(' %Y-%m-%d '))
        x = re.sub(ur'[年月]',  '/', x)
        x = re.sub(ur'[日]',    ' ', x)
        x = re.sub(ur'\s{2,}', r' ', x)

        # XX前
        res = ( re.search(ur'(?P<S>\d+)\s*秒钟?前', x) \
             or re.search(ur'(?P<M>\d+)\s*分钟前', x) \
             or re.search(ur'(?P<H>\d+)\s*小时前', x) \
             or re.search(ur'(?P<d>\d+)\s*天前', x) \
             or re.search('', '')).groupdict()

        if res:
            dt = now - timedelta(
                                days    = int(res.get('d', 0)),
                                hours   = int(res.get('H', 0)),
                                minutes = int(res.get('M', 0)),
                                seconds = int(res.get('S', 0))
                              )
        else:
            # XX-XX-XX XX:XX:XX
            res = ( re.search(ur'(?P<Y>\d+)[/-](?P<m>\d+)[/-](?P<d>\d+)(\s+(?P<H>\d{2}):(?P<M>\d{2})(:(?P<S>\d{2}))?)?', x) \
                 or re.search('', '')).groupdict()

            if res:
                Y = res.get('Y', now.year)
                m = res.get('m', now.month)
                d = res.get('d', now.day)
                H = res.get('H', now.hour)
                M = res.get('M', now.minute)
                S = res.get('S', 0)

                dt = datetime(
                            year   = int(Y) if Y!=None else now.year,
                            month  = int(m) if m!=None else now.month,
                            day    = int(d) if d!=None else now.day,
                            hour   = int(H) if H!=None else now.hour,
                            minute = int(M) if M!=None else now.minute,
                            second = int(S) if S!=None else 0
                        )
            else:
                # 1970-01-01 00:00:00
                dt = datetime.utcfromtimestamp(0)+offset

    # UNIX TIMESTAMP
    elif fmt=='unix':
        dt = datetime.utcfromtimestamp(int(data))
        offset = timedelta(0)
    else:
        dt = datetime.strptime(unicode(data).encode('utf-8'), unicode(fmt).encode('utf-8'))

    return dt-offset

def tz_offset(tz):
    res = (re.search(r'(?P<F>[-+])(?P<H>\d{2}):?(?P<M>\d{2})', tz) or re.search('', '')).groupdict()
    offset = (1 if res.get('F', '+')=='+' else -1) * timedelta(
                        hours   = int(res.get('H', 0)),
                        minutes = int(res.get('M', 0)))
    return offset

def filter_data(query, data):
    for k,v in query.iteritems():
        if k=='delta':
            now = datetime.utcnow()
            if not (type(data)==datetime and (now-data).total_seconds()<v):
                return False
        elif k=='match':
            if not (type(data) in [str, unicode] and re.match(v, data)):
                return False
        elif k=='min':
            if data<v:
                return False
        elif k=='max':
            if data>v:
                return False
        else:
            logging.log(logging.WARNING,u'invalid query <%s>'%(query))
            return False
    return True

###连接数据库并添加数据###
def connect_uri(uri):

    if uri.startswith('mysql://'):
        try:
            import mysql.connector as pymysql
        except ImportError:
            import pymysql
        parsed = urlparse.urlparse(uri)
        host = parsed.hostname
        port = parsed.port
        user = parsed.username
        passwd = parsed.password

        db, tbl = parsed.path.strip('/').split('.')
        cnn = pymysql.connect(
                                host=host,
                                port=port,
                                user=user,
                                passwd=passwd,
                                db=db,
                                charset='utf8'
                             )
    elif uri.startswith('mongodb://'):
        import pymongo
        parsed = pymongo.uri_parser.parse_uri(uri)
        database = parsed['database']
        collection = parsed['collection']
        host, port = parsed['nodelist'][0]

        cnn = pymongo.MongoClient(host=host, port=port)
        db = cnn[database]
        tbl = db[collection]

    return (cnn, db, tbl)
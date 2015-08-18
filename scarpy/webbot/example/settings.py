#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# A simple spider written by Kev++

BOT_NAME = 'example'
LOG_LEVEL = 'INFO'

SPIDER_MODULES = ['example.spiders']
NEWSPIDER_MODULE = 'example.spiders'

USER_AGENT = 'Mozilla/5.0 (w3660t by Kev++)'

DEFAULT_REQUEST_HEADERS = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh,en;q=0.5',
        }

ITEM_PIPELINES = [
            'example.pipelines.BasicPipeline',
            'example.pipelines.DebugPipeline',
            'example.pipelines.MongoPipeline',
            'example.pipelines.MysqlPipeline',
            'example.pipelines.ZmqPipeline',
        ]

EXTENSIONS = {
            'example.extensions.StatsPoster': 999
        }

DOWNLOADER_MIDDLEWARES = {
            'example.middlewares.ProxyMiddleware': 999,
            'scrapy.contrib.downloadermiddleware.retry.RetryMiddleware': None,
            'example.middlewares.RetryMiddleware': 500,
        }

SPIDER_MIDDLEWARES = {
            'example.middlewares.DedupMiddleware': 999
        }

TELNETCONSOLE_ENABLED = False
DOWNLOAD_TIMEOUT = 30
RETRY_TIMES = 2

DEFAULT_LOGGER = 'mongodb://192.168.3.175:27017/result.data'
DEFAULT_DEDUP = None


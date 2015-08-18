from scrapy import cmdline

cmdline.execute("scrapy crawl example -a config=http://10.6.2.124/conf/yuqing/huxiwang.conf -a debug=true".split())

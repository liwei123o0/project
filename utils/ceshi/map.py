# -*- coding: utf-8 -*-
# ! /usr/bin/env python

from multiprocessing.dummy import Pool as Threadpoll
import urllib2
from lxml import etree
import time
def gethtml(url):
    html =urllib2.urlopen(url).read()
    dom = etree.HTML(html)
    title = dom.xpath("(//a[@class='p_author_name sign_highlight j_user_card vip_red '])[1]|(//a[@class='p_author_name sign_highlight j_user_card'])[1]")
    for i in  title:
        return i.text
urls=[]
for i in range(1,27):
    newurl ="http://tieba.baidu.com/p/3854692202?pn=%s" % i
    urls.append(newurl)
start =time.time()
for url in urls:
    print url
    gethtml(url)
stop =time.time()
print "单线程用时：%s" %(stop-start)


poll =Threadpoll(1)
start =time.time()
requests =poll.map(gethtml,urls)
poll.close()
poll.join()
for name in  requests:
    print name
stop =time.time()

print "多线程用时：%s"%(stop-start)

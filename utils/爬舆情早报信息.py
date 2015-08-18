# -*- coding:utf-8 -*-
import urllib2
import urllib
import cookielib
from lxml import etree
import time
import json
import re
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
###登陆入口地址设置
url= "http://yqms.yqzbw.com/apps/yqzb/LoginOK.do?userid=%E9%99%95%E8%A5%BF%E7%89%B9%E4%BF%A1&passwd=2AA7981633EBECF07D8EE07850A5E211&logintype=login"
#主方法
def conn(url):
    address = "/data/news/news0/" #爬取存放位置
    url = url
    ##采集页面设置
    newUrl = ["http://yqms.yqzbw.com/apps/yqzb/Listyqkb.do?sourcetype=01&orientation=1,2,3,4&hotwords=1","http://yqms.yqzbw.com/apps/yqzb/Listyqkb.do?sourcetype=01&orientation=2&hotwords=1","http://yqms.yqzbw.com/apps/yqzb/Listyqkb.do?sourcetype=02&orientation=1,2,3,4&hotwords=1","http://yqms.yqzbw.com/apps/yqzb/Listyqkb.do?sourcetype=02&orientation=2&hotwords=1","http://yqms.yqzbw.com/apps/yqzb/Listyqkb.do?sourcetype=03&orientation=1,2,3,4&hotwords=1","http://yqms.yqzbw.com/apps/yqzb/Listyqkb.do?sourcetype=03&orientation=2&hotwords=1","http://yqms.yqzbw.com/apps/yqzb/Listyqkb.do?sourcetype=05&orientation=1,2,3,4&hotwords=1","http://yqms.yqzbw.com/apps/yqzb/Listyqkb.do?sourcetype=05&orientation=2&hotwords=1","http://yqms.yqzbw.com/apps/yqzb/Listyqkb.do?sourcetype=06&orientation=1,2,3,4&hotwords=1","http://yqms.yqzbw.com/apps/yqzb/Listyqkb.do?sourcetype=06&orientation=2&hotwords=1","http://yqms.yqzbw.com/apps/yqzb/Listyqkb.do?sourcetype=07&orientation=1,2,3,4&hotwords=1","http://yqms.yqzbw.com/apps/yqzb/Listyqkb.do?sourcetype=07&orientation=2&hotwords=1"]
    enable_proxy = False
    null_proxy_handler = urllib2.ProxyHandler({})
    if enable_proxy:
        opener = urllib2.build_opener(proxy_handler)
    else:
        opener = urllib2.build_opener(null_proxy_handler)
    urllib2.install_opener(opener)
#添加头信息
    headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
    'Content-Type':'application/x-www-form-urlencoded',
    'Host':'yqms.yqzbw.com',
    'Referer':'http://www.yqzbw.com/'
            }
#提交表单内容
    values = {
        'logintype':'1',
        'userid':'陕西特信',
        'password':'117118',
            }
#表单编码
    data = urllib.urlencode(values)
#保存cookie信息
    cookieJar=cookielib.CookieJar()
    opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
    req = urllib2.Request(url,headers=headers,data=data)
    result = opener.open(req)
#在新的页面使用cookie
    Newtime = time.strftime('%Y%m%d%H%M',time.localtime(time.time()))
    for page in newUrl:
        result = opener.open(page)
        HTML = result.read()
        Tree = etree.HTML(HTML)
        for i in Tree.xpath('//div[@class="dl_linst"]/dl/dt/a'):
            Requrl = "http://yqms.yqzbw.com/apps/yqzb/"+i.attrib['href']
            with open(address+str(Newtime)+".json",'a') as f:
                result = opener.open(Requrl)
                HTML = result.read()
                NewTree = etree.HTML(HTML)
                for new in NewTree.xpath('//div[@class="yl_content_L_wra"]/div'):
                    #具体页面数据采集存储在字典当中
                    SQMY = {}
                    SQMY['IR_SRCNAME'] = "舆情早报"
                    if "type=01" in page:
                        SQMY['IR_GROUPNAME'] = "国内新闻"
                    elif "type=02" in page:
                        SQMY['IR_GROUPNAME'] = "国内论坛"
                    elif "type=03" in page:
                        SQMY['IR_GROUPNAME'] = "国内博客"
                    elif "type=05" in page:
                        SQMY['IR_GROUPNAME'] = "国内新闻_电子报"
                    elif "type=06" in page:
                        SQMY['IR_GROUPNAME'] = "微信"
                    elif "type=07" in page:
                        SQMY['IR_GROUPNAME'] = "国内视频"
                    else:
                        pass
                    SQMY['IR_CATALOG2'] = "舆情早报2"
                    ##需要格式化的内容
                    SQMY['IR_URLTITLE'] = ''.join(new.xpath('./h1/text()'))
                    SQMY['IR_CONTENT'] = ''.join(new.xpath('./div[1]/text()'))
                    SQMY['IR_URLTIME'] = ''.join(new.xpath('./h2/div/span[2]/text()'))
                    SQMY['IR_SITENAME'] = ''.join(new.xpath('./h2/div/span[1]/text()'))
                    SQMY['IR_URLNAME'] = ''.join(new.xpath('./p/a/text()'))
                    ###格式化数据
                    SQMY['IR_URLTIME'] = re.sub('时间：','',str(SQMY['IR_URLTIME']))
                    SQMY['IR_SITENAME'] = re.sub('来源:','',str(SQMY['IR_SITENAME']))
                    SQMY['IR_SITENAME'] = re.sub(r'\[域名\]','',str(SQMY['IR_SITENAME']))
                    SQMY['IR_SITENAME'] = re.sub('【','',str(SQMY['IR_SITENAME']))
                    SQMY['IR_SITENAME'] = re.sub('】','',str(SQMY['IR_SITENAME']))
                    SQMY['IR_SITENAME'] = re.sub(r'\？','',str(SQMY['IR_SITENAME']))
                    SQMY['IR_SITENAME'] = re.sub(r'-$','',str(SQMY['IR_SITENAME']))
					###区分百度贴吧与论坛####
                    #print type(SQMY['IR_SITENAME'])
                    if u'百度贴吧' in SQMY['IR_SITENAME']:
					    SQMY['IR_GROUPNAME'] = '百度贴吧'
                    #print SQMY['IR_GROUPNAME']
                    ####测试###
                    #print SQMY['IR_SITENAME']
                    #print SQMY['IR_URLTITLE']
                    #print SQMY['IR_CONTENT']
                    #######
                    EnSqmy = json.dumps(SQMY)
                    f.write(EnSqmy)
                    f.write("\n")
    with open(address+str(Newtime)+".json.ok",'w') as a:
        a.write("")
while 1:
    conn(url)
    time.sleep(30)

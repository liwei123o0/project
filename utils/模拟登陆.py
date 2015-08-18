# -*- coding: utf-8 -*-
#! /usr/bin/env python
import requests
data ={
    '__EVENTARGUMENT':'',
    '__EVENTTARGET':'',
    '__EVENTVALIDATION':'/wEdAAUIqCk3Gcmu25zI9fQWqoC7hI6Xi65hwcQ8/QoQCF8JIahXufbhIqPmwKf992GTkd0wq1PKp6+/1yNGng6H71Uxop4oRunf14dz2Zt2+QKDEM3sbzJLySdZoy08+/dzW8VF2on0',
    '__VIEWSTATE':'	/wEPDwUKLTM1MjEzOTU2MGQYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgEFC2Noa1JlbWVtYmVy4b/ZXiH+8FthXlmKpjSEgi7XBNU=',
    '__VIEWSTATEGENERATOR':'	C2EE9ABB',
    'btnLogin':'	登 录',
    'tbPassword':'liwei123@asd',
    'tbUserName':'liwei123o0',
    'txtReturnUrl':'http://www.cnblogs.com/'
}
s =requests.session()
s.post(url='http://passport.cnblogs.com/login.aspx',data=data)

r=s.get('http://home.cnblogs.com/group/')
print r.text


# -*- coding:utf-8 -*-
import urllib2
import urllib
import cookielib
from lxml import etree
##添加代理
url= "http://yqms.yqzbw.com/apps/yqzb/LoginOK.do?userid=%E9%99%95%E8%A5%BF%E7%89%B9%E4%BF%A1&passwd=2AA7981633EBECF07D8EE07850A5E211&logintype=login"
def conn(url):
    url = url
    enable_proxy = False
    proxy_handler = urllib2.ProxyHandler({"http" : 'http://10.6.6.229:3128'})
    null_proxy_handler = urllib2.ProxyHandler({})
    if enable_proxy:
        opener = urllib2.build_opener(proxy_handler)
    else:
        opener = urllib2.build_opener(null_proxy_handler)
    urllib2.install_opener(opener)
#添加头信息
    headers = {
    #'Host':'passport.cnblogs.com',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
    #'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    #'Connection':'keep-alive'
    'Content-Type':'application/x-www-form-urlencoded',
    'Host':'yqms.yqzbw.com',
    #'User-Agent':'MicroMessenger Client',
    'Referer':'http://www.yqzbw.com/'
            }
#提交表单内容
    values = {
        #'__VIEWSTATE':'/wEPDwUKLTM1MjEzOTU2MGQYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgEFC2Noa1JlbWVtYmVy4b/ZXiH+8FthXlmKpjSEgi7XBNU=',
        #'__VIEWSTATEGENERATOR':'C2EE9ABB',
        #'__EVENTVALIDATION':'/wEdAAUIqCk3Gcmu25zI9fQWqoC7hI6Xi65hwcQ8/QoQCF8JIahXufbhIqPmwKf992GTkd0wq1PKp6+/1yNGng6H71Uxop4oRunf14dz2Zt2+QKDEM3sbzJLySdZoy08+/dzW8VF2on0',
        #'tbUserName':'liwei123o0',
        #'tbPassword':'liwei123@asd',
        #'btnLogin':'登陆',
        #'txtReturnUrl':'http://www.cnblogs.com/',
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

    result = opener.open(newUrl)
    HTML = result.read()
    Tree = etree.HTML(HTML)
    for i in Tree.xpath('//div[@class="dl_linst"]/dl/dt/a'):
        print i.text
conn(url)





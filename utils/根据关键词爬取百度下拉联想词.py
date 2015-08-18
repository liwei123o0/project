# -*- coding: utf8 -*-
#! /usr/bin/env python
import urllib2
import re
import json
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
headers ={
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
}
with open('keywords.txt','r')as f:
    for keywords in f.readlines():
        l=keywords.replace('\n','')
        r=l.replace(' ','%20')
        key=r.replace('\t','')
        req = urllib2.Request\
            ('http://suggestion.baidu.com/su?wd=%s&json=1&p=3&sid=11205_11210_1435_11333_10773_10488_11071_11276_11240_11280_11151_11243_11256_10618&req=2&cb=jQuery110209117847587913275_1422352631205&_=1422352631219'%key,headers=headers)
        try:
            response =urllib2.urlopen(req)
            body = response.read()
            b=str(body.decode('gbk',errors='ignore').splitlines())
            a = re.compile(r'(?<="s":)\[[^}]+')
            c= a.search(b)
            d=c.group()
            j =json.loads(d)
            for i in range(len(j)):
                a=(j[i])
                print(a)
                with open('baidu.txt','a')as w:
                    w.write(a)
                    w.write('\n')
        except:
            print('错误关键字：'+key)
            with open('error.txt','a')as e:
                e.write(key+'\n')
            continue
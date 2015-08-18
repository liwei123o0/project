# -*- coding: utf-8 -*-
#! /usr/bin/env python

import urllib2
import re
from lxml import etree
from multiprocessing.dummy import Pool
def scrapy():
    dws =['工信厅','住建厅','交通厅','农业厅','卫计委','工商局','质监局','食药局','旅游局']
    ds = ['西安市','宝鸡市','渭南市','咸阳市','铜川市','榆林市','延安市','安康市','汉中市','商洛市','杨凌农业示范区','韩城市','西咸新区']
    with open("keywords.txt","rb")as f:
        key = f.read()
    keys =re.split('、',key)
    for d in ds:
        for j in dws:
            for i in keys:
                word = '"%s"+"%s"+"%s"'%(d,j,i)
                words = urllib2.quote(word)
                url = "http://news.baidu.com/ns?ct=1&rn=20&ie=utf-8&rsv_bp=1&sr=0&cl=2&f=8&prevct=no&tn=news&word=%s&rsv_sug3=3&rsv_sug4=149&rsv_sug1=4&rsv_sug2=0&inputT=1904&rsv_sug=2"% words
                html =urllib2.urlopen(url,timeout=10).read()
                dom =etree.HTML(html)
                data =dom.xpath("//span[@class='nums']/text()")
                data =re.findall(r'\d+',data[0].replace(',',''))[0]
                with open("ceshi3.txt","ab")as w:
                    w.write('%s:\t%s\n'%(word,data.encode("utf8")))
                print '%s:\t%s'%(word,data.encode("utf8"))
#分词
def fenci(name,num,wj):

    with open("ceshi.txt",'r')as f:
        keywords =f.readlines()
    for keyword in keywords:
        words =re.split(r':',keyword)
        with open(wj,'ab')as w:
            w.write(words[num].replace('\t','')+name)
#组关键词
def gjc():
    ds = ['西安市']
    dwss =['工信厅','住建厅','交通厅','农业厅','卫计委','工商局','质监局','食药局','旅游局']
    dws =[
        ['工信局','工业和信息化局'],['住建局','住房和城乡建设局'],['交通局','交通运输局','交通运输委员会','交委'],['农业局','农业和科学技术局'],
        ['卫计委','卫生和计划生育委员会'],['工商局','工商行政管理局'],['质监局','质量技术监督局'],['食药局','药监局','食品药品监督管理局'],['旅游局','旅游管理局']
          ]
    with open("keywords.txt","rb")as f:
        key = f.read()
    keys =re.split('、',key)
    # for d in ds:
    for w in dws:
        for k in keys:
            word = '"西安市"+"%s"+"%s"'%(w,k)
            words = urllib2.quote(word)
            url = "http://news.baidu.com/ns?ct=1&rn=20&ie=utf-8&rsv_bp=1&sr=0&cl=2&f=8&prevct=no&tn=news&word=%s&rsv_sug3=3&rsv_sug4=149&rsv_sug1=4&rsv_sug2=0&inputT=1904&rsv_sug=2"% words
            html =urllib2.urlopen(url,timeout=10).read()
            dom =etree.HTML(html)
            data =dom.xpath("//span[@class='nums']/text()")
            data =re.findall(r'\d+',data[0].replace(',',''))[0].encode("utf8")
                # with open("ceshi.txt","ab")as w:
                #     w.write('%s:\t%s\n'%(word,data.encode("utf8")))
            print '%s:\t%s'%(word,data)
            w= open("ceshi.txt",'ab')
            w.write( '%s:\t%s\n'%(word,data))
    w.close()
# gjc()
# fenci('\n',0,'1.txt')
# fenci('',1,'2.txt')
dsj=[]
dws =[
    ['工信局','工业和信息化局'],['住建局','住房和城乡建设局'],['交通局','交通运输局','交通运输委员会','交委'],['农业局','农业和科学技术局'],
    ['卫计委','卫生和计划生育委员会'],['工商局','工商行政管理局'],['质监局','质量技术监督局'],['食药局','药监局','食品药品监督管理局'],['旅游局','旅游管理局']
]
ds = ['西安市','汉中市']
for s in ds:
    for d in dws:
        for i in d:
            word = '"%s"+"%s"'%(s,i)
            dsj.append(word)
with open("keywords.txt","rb")as f:
    key = f.read()
    keys =re.split('、',key)
for i in range(40,42):
    for j in keys:
        word = '%s+"%s"'%(dsj[i],j)
        words = urllib2.quote(word)
        url = "http://news.baidu.com/ns?ct=1&rn=20&ie=utf-8&rsv_bp=1&sr=0&cl=2&f=8&prevct=no&tn=news&word=%s&rsv_sug3=3&rsv_sug4=149&rsv_sug1=4&rsv_sug2=0&inputT=1904&rsv_sug=2"% words
        html =urllib2.urlopen(url,timeout=10).read()
        dom =etree.HTML(html)
        data =dom.xpath("//span[@class='nums']/text()")
        data =re.findall(r'\d+',data[0].replace(',',''))[0].encode("utf8")
        # with open("ceshi.txt","ab")as w:
        #     w.write('%s:\t%s\n'%(word,data.encode("utf8")))
        print '%s:\t%s'%(word,data)
        w= open("ceshi.txt",'ab')
        w.write( '%s:\t%s\n'%(word,data))
w.close()
fenci('\n',0,'1.txt')
fenci('',1,'2.txt')
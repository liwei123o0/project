# -*- coding: utf-8 -*-
#! /usr/bin/env python
import re
a ="('华晨宝马','http://dealer.autohome.com.cn/128782/','西安中宝','西安中宝'),"

with open("car.txt","r")as f:
    b = f.read()
    c= b.decode("gb2312")
    d = c.split("\n")
    for e in d:
        f =re.split("\s+",e)
        insert = "('%s','%s','%s','%s')," %(f[2],f[3],f[1],f[0],)
        print insert
# -*- coding: utf-8 -*-
#! /usr/bin/env python
import re
import time
import datetime
import sys
def test():
    times = "05月05日 20:27"
    month = int(re.findall("[0-9]+",times)[0])
    if month > datetime.datetime.now().month:
        times = "2015-"+times.replace("月","-").replace("年","-").replace("日","")
        print times
    else:
        times = "2016-"+times.replace("月","-").replace("年","-").replace("日","")
        print times
if __name__ =="__main__":
    test()
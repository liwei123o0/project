# -*- coding: utf-8 -*-
#! /usr/bin/env python

with open("dys.txt","rb") as f :
    keywords = f.readlines()

for word in keywords:
    word = word.replace("\r\n","")
    print word
    with open("bds.txt","a")as w:
        w.write('"%s" OR ' %word)

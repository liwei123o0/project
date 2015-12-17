# -*- coding: utf-8 -*-
#! /usr/bin/env python
def loadword():
    with open("E:\projectall\project\keyword.txt","rb")as f:
        words = f.readlines()
    return words
def joinurl():
    words = loadword()
    for word in words:
        word = word.replace("\r\n","")
        url = "".join("http://weixin.sogou.com/weixin?type=2&query=%s&ie=utf8&tsn=1"% word,)
        with open("url.txt","a+")as w:
            w.write(url+"\n")
joinurl()
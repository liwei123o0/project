# -*- coding: utf-8 -*-
#! /usr/bin/env python
import spynner
browser = spynner.Browser()
#创建一个浏览器对象
# browser.hide()
browser.show()
#打开浏览器，并隐藏。

browser.load(u"http://s.weibo.com/wb/西安杀人&xsort=time&Refer=weibo_wb")
#browser 类中有一个类方法load，可以用webkit加载你想加载的页面信息。
#load(是你想要加载的网址的字符串形式)
html= browser.html.encode("utf-8")
#browser 类中有一个成员是html，是页面进过处理后的源码的字符串.
#将其转码为UTF-8编码
with open("weibo.txt","w")as w:
    w.write(html)
#你也可以将它写到文件中，用浏览器打开。
browser.close()
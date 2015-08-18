# -*- coding: utf-8 -*-
#! /usr/bin/env python

from snownlp import SnowNLP
from snownlp import sentiment
# sentiment.train('C:\\Python27\\Lib\\site-packages\\snownlp-0.12.1-py2.7.egg\\snownlp\\sentiment\\neg.txt', 'C:\\Python27\\Lib\\site-packages\\snownlp-0.12.1-py2.7.egg\\snownlp\\sentiment\\pos.txt')
# sentiment.save('C:\\Python27\\Lib\\site-packages\\snownlp-0.12.1-py2.7.egg\\snownlp\\sentiment\\sentiment.marshal')
with open("fm.txt","r")as f:
    txts =f.readlines()
i=0
for txt in txts:
    i+=1
    s =SnowNLP(txt)
    print "%s:\t"%i+str(s.sentiments)
#
# s =SnowNLP(u"价格合理，不满意")
# print s.sentiments
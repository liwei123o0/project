# coding=utf8
__author__ = 'liwei'
import re
'''
读取文本文件的关键词，然后在把对应的字符串的连接中的某个位置字符串替换掉，然后写入到另一个文本文件中
'''

with open('E:\url.txt','rb') as rs:
    a=rs.readlines()
    for url in a:
        urln=url.strip('\n')
        b='http://sou.autohome.com.cn/luntan?q=%CE%F7%B0%B2&entry=40&class=0&ClassId=0&order=score&time='
        strinfo = re.compile('%CE%F7%B0%B2')
        c=strinfo.sub(urln,b)
        with open('E:\url1.txt','ab') as ws:
            ws.writelines(c+'\n')
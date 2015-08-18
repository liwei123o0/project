# -*- coding: utf-8 -*-
# ! /usr/bin/env python
import re
import json

# 在 serverData 中查找 server time 和 nonce
# 解析过程主要使用了正则表达式和JSON
def sServerData(serverData):
    p = re.compile('\((.*)\)')    # 定义正则表达式
    jsonData = p.search(serverData).group(1)  # 通过正则表达式查找并提取分组1
    data = json.loads(jsonData)
    serverTime = str(data['servertime'])   # 获取data中的相应字段，Json对象为一个字典
    nonce = data['nonce']
    pubkey = data['pubkey']
    rsakv = data['rsakv']  # 获取字段
    return serverTime, nonce, pubkey, rsakv


#Login中解析重定位结果部分函数
def sRedirectData(text):
    p = re.compile('location\.replace\([\'"](.*?)[\'"]\)')
    loginUrl = p.search(text).group(1)
    print 'loginUrl:',loginUrl   # 输出信息，若返回值含有 'retcode = 0' 则表示登录成功
    return loginUrl
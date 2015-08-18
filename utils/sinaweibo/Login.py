# -*- coding: utf-8 -*-
# ! /usr/bin/env python
import WeiboLogin
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

username = 'leo.liu@9i2.com.cn'
pwd = '080808'

def login():
    #我的新浪微博的用户名和密码
    weibologin = WeiboLogin.WeiboLogin(username, pwd)   #调用模拟登录程序
    if weibologin.Login():
        print u"登陆成功..！"  #此处没有出错则表示登录成功
    else:
        print u"登陆失败..!"
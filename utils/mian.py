# -*- coding: utf-8 -*-
#! /usr/bin/env python
import weiboLogin
import urllib
import urllib2
import time

filename = 'config.txt'#保存微博账号的用户名和密码，第一行为用户名，第二行为密码

WBLogin = weiboLogin.weiboLogin()
if WBLogin.login(filename)==1:
    print 'Login success!'
else:
    print 'Login error!'
    exit()
# -*- coding: utf-8 -*-
#! /usr/bin/env python
import requests

headers={
    'Cookie':'s%3AYE04xsiaWQ9xvFoKANaNwiEL.r7ZyHT9bOv182Mziq%2FxhDPW%2BznFBJ8Ilun5zadgHnok; Filtering=0.0; Filtering=0.0; simsimi_uid=88163218; simsimi_uid=88163218; selected_nc=ch; selected_nc=ch; menuType=web; menuType=web; __utma=119922954.333221998.1422345294.1422345294.1422345294.1; __utmb=119922954.34.9.1422347199801; __utmc=119922954; __utmz=119922954.1422345294.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
    'Referer':'http://www.simsimi.com/talk.htm?lc=ch',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
    }
ms=['王文彬','亚子','很好']
for msg in ms:
    url ='http://www.simsimi.com/func/reqN?lc=ch&ft=0.0&req=%s&fl=http://www.simsimi.com/talk.htm'%msg
    r=requests.get(url=url,headers=headers)
    print r.json()['sentence_resp']
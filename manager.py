# -*- coding: utf-8 -*-
#! /usr/bin/env python

import  MySQLdb
def tongji(nf):
    dss = [u'西安',u'宝鸡',u'渭南',u'咸阳',u'铜川',u'榆林',u'延安',u'安康',u'汉中',u'商洛',u'杨凌农业示范区',u'韩城',u'西咸新区']
    zfms = [u'A3',u'B3',u'C3']
    dws =[u'工信委',u'住建局',u'交通局',u'农业局',u'卫计委',u'工商局',u'质监局',u'药监局',u'旅游局']
    conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd='root',db='',charset='utf8')
    cur = conn.cursor()
    for dw in dws:
        for ds in dss:
            for zfm in zfms:
                # print dw,zfm,ds
                news = u"SELECT COUNT(*) FROM fenxi.news14 WHERE 涉及单位='%s' AND 事件性质='%s' AND 地域='%s'"%(dw,zfm,ds)
                cur.execute(news)
                n = cur.fetchall()[0][0]
                weixin = u"SELECT COUNT(*) FROM fenxi.weixin  WHERE   涉及单位='%s' AND 事件性质='%s' AND 地域='%s' AND 日期 LIKE '%%%s%%'" %(dw,zfm,ds,nf)
                cur.execute(weixin)
                wx = cur.fetchall()[0][0]
                bbs = u"SELECT COUNT(*) FROM fenxi.bbs  WHERE   涉及单位='%s' AND 事件性质='%s' AND 地域='%s' AND 日期 LIKE '%%%s%%'" %(dw,zfm,ds,nf)
                cur.execute(bbs)
                b = cur.fetchall()[0][0]
                # print b
                weibo = u"SELECT COUNT(*) FROM fenxi.weibo  WHERE   涉及单位='%s' AND 事件性质='%s' AND 地域='%s' AND 日期 LIKE '%%%s%%'" %(dw,zfm,ds,nf)
                cur.execute(weibo)
                wb = cur.fetchall()[0][0]
                # print wb
                zf = int(n)+int(wx)+int(wb)+int(b)
                # print "%s+%s+%s:%s" %(dw,zfm,ds,zf)
                print zf
    cur.close()
    conn.close()

def biao(num,numm):
    str=[]
    for i in xrange(num,numm,3):
        c = "F%s" %i
        f = "G%s" %i
        ii = "H%s" %i
        # l = "N%s" %i
        # o = "Q%s" %i
        # r = "T%s" %i
        # u = "W%s" %i
        # x = "Z%s" %i
        # aa = "AC%s" %i
        str.append(c)
        str.append(f)
        str.append(ii)
        # str.append(l)
        # str.append(o)
        # str.append(r)
        # str.append(u)
        # str.append(x)
        # str.append(aa)
    stri =  "+".join(str)
    return "="+stri
if __name__ =='__main__':
    # tongji(2014)
    print biao(4,41)
    print biao(5,42)
    print biao(6,43)
    # for i in xrange(4,41,3):
    #     print i
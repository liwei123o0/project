# -*- coding=utf-8 -*-
import MySQLdb
try:
    conn = MySQLdb.connect(host='10.6.2.79',user='root',passwd='123@asd',db='WEBSITE_WEIXIN',charset='utf8')
    cur = conn.cursor()
    sql = "insert into WEBSITE_WEIXIN.DEALER_DIM(MAKE,DEALER,SCREEN_NAME,SEARCHED_URL,CLASS,PROVINCE,CITY) values(%s,%s,%s,%s,'中档车','陕西','西安')"
    data = []
    with open('2.txt','r') as f:
        for line in f.readlines():
            data1=tuple(line.split())
            data.append(data1)
        print data
    cur.executemany(sql,data)
    conn.commit()
    cur.close()
    conn.close()
except MySQLdb.Error,e:
    print "Mysql Error %d: %s" % (e.args[0], e.args[1])

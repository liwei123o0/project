# -*- coding: utf-8 -*-
'''
mysql数据库操作，依赖包可以通过   下载然后导入
'''
import MySQLdb
import threading

conn= MySQLdb.connect(
	host='localhost',
	port = 3306,
	user='root',
	passwd='root',
	db ='',
	)
cur = conn.cursor()
def findMin():
	#存入数据库以后，从数据库里面从id最小的开始获取，写入数据库。
	print "isfind"
	sql = u"select url from test.get_url  where is_geted = 0 order by id desc limit 10"
	cur.execute(sql)
	res1 = cur.fetchall()
	for i in range(10):
		print res1[i][0]
if __name__ == '__main__':
    for i in xrange(10):
        t =threading.Thread(target=findMin())
        t.setDaemon(True)
        t.start()

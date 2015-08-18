# -*- coding: utf-8 -*-
# ! /usr/bin/env python
import paramiko
import MySQLdb
import time
import os
#远程执行命令
def sshlinux(host,username,passwd,port,cmd):
    #远程执行命令
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host,port,username, passwd)
    #远程命令
    stdin, stdout, stderr = ssh.exec_command(cmd)
    #打印输出结果
    # print stdout.readlines()
    ssh.close()
#远程上传文件
def sftplinux(host,username,passwd,port):
    t = paramiko.Transport(host,port)
    t.connect(username = username, password = passwd)
    sftp = paramiko.SFTPClient.from_transport(t)
    remotepath='/home/lw/project/configs/keywords/keywords.txt'
    localpath='E:\project\ceshi\keywords.txt'
    sftp.put(localpath,remotepath)
    t.close()
#与数据库同步keywords关键词
def mysql():
    conn = MySQLdb.connect(host="10.6.2.121",port=3306,user="root",passwd="root",charset="utf8")
    cur=conn.cursor()
    cur.execute(u"SELECT keyword FROM weibo.keyword;")
    name =cur.fetchall()
    if os.path.exists("E:\project\ceshi\keywords.txt"):
            os.remove("E:\project\ceshi\keywords.txt")
    for i in name:
        # print i[0]
        with open("keywords.txt","ab")as w:
            w.write(i[0].encode("utf8")+"\n")
    cur.close()
    conn.close()
#同步数据库关键词到10.6.2.124
if __name__=="__main__":
    rm ="rm -rf /home/lw/project/configs/keywords/keywords.txt"
    chmod ="chmod 755 /home/lw/project/configs/keywords/*.txt"
    start =time.time()
    mysql()
    sshlinux("10.6.2.124","lw","root",22,rm)
    sftplinux("10.6.2.124","lw","root",22)
    sshlinux("10.6.2.124","lw","root",22,chmod)
    stop =time.time()
    print "ok 用时：%s"% (stop-start)

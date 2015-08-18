# -*- coding: utf-8 -*-
#! /usr/bin/env python
from flask import Flask,render_template,request,redirect

from sinawb.src import phantomjs

application =Flask(__name__)
datalist =[]
@application.route("/")
def websearch():
    return render_template("index.html",datalist=datalist)
@application.route('/post',methods=['POST'])
def get_keyword():
    keywords = request.form.get("keywords")
    keyword = keywords.encode("utf8")
    if keywords=="":
        return redirect('/')
    else:
        data = phantomjs.dtwb(keyword)
        save(data)
        return redirect('/')
def save(data):
    datalist.append(data)
if __name__=='__main__':
    application.run('0.0.0.0',80)
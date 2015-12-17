# -*- coding: utf-8 -*-
#! /usr/bin/env python

from datetime import datetime
from flask import render_template, session, redirect, url_for,flash
from forms import NameForm
from .. import db
from ..models import User
from . import main
@main.route('/',methods=['GET','POST'])
def index():
    form = NameForm(csrf_enabled=False)
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            flash(u'数据表里面无此姓名，添加进数据库！')
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False

        else:
            flash(u'数据库此人姓名已存在,不做重复添加!')
            session['known'] = True

    #     old_name = session.get('name')
    #     if old_name is not None and old_name !=form.name.data:
    #         flash(u'你居然修改自己的名字，你妈知道吗？')
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('main.index'))

    #将数据传值给前段页面引用
    return render_template('index.html',
                           current_time=datetime.utcnow(),
                           form=form,
                           name=session.get('name'),
                           known = session.get('known',False))



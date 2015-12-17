# -*- coding: utf-8 -*-
#! /usr/bin/env python

#处理表单
from flask_wtf import Form
from wtforms import StringField,SubmitField,PasswordField,BooleanField
from wtforms.validators import DataRequired,Length,Email

#创建了文本框和提交按钮
class NameForm(Form):
    #DataRequired验证是否有数据输入
    name = StringField(u'你是谁?',validators=[DataRequired()])
    submit = SubmitField(u'提交')

class LoginForm(Form):
    email = StringField(u'邮箱登陆',validators=[DataRequired(),Length(1,64),Email()])
    password = PasswordField(u'密码',validators=[DataRequired()])
    remember_me = BooleanField(u'允许登陆')
    submit = SubmitField(u'登陆')
# -*- coding: utf-8 -*-
#! /usr/bin/env python

#处理表单
from flask_wtf import Form
from wtforms import StringField,SubmitField,PasswordField,BooleanField
from wtforms.validators import DataRequired,Length,Email,Regexp,EqualTo
from wtforms import ValidationError
from ..models import User


#创建了文本框和提交按钮
class LoginForm(Form):
    email = StringField(u'邮箱登陆',validators=[DataRequired(),Length(1,64),Email(message=u'请输入正确的邮箱账号！')])
    password = PasswordField(u'密码',validators=[DataRequired()])
    remember_me = BooleanField(u'记住我')
    submit = SubmitField(u'登陆')


#创建注册用户表单
class RegistrationForm(Form):
    eamil = StringField(u'邮箱',validators=[DataRequired(),Length(1,64),Email(message=u'请输入正确的邮箱格式！')])
    username = StringField(u'昵称',validators=[DataRequired(),Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,u'只允许包含字母、数字、下划线、点号')])
    password = PasswordField(u'密码',validators=[DataRequired(),EqualTo('password2',u'密码不一致！')])
    password2 = PasswordField(u'在输入一次!',validators=[DataRequired()])
    submit = SubmitField(u'注册')
    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(u'该邮箱已存在！')
    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(u'此用户名已存在!')

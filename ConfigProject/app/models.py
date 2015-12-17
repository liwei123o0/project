# -*- coding: utf-8 -*-
#! /usr/bin/env python

from .import db
from flask import current_app
#用户令牌环账户认证
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
#注册用户密码加密
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager


#数据模型定义
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    username = db.Column(db.String(64),unique=True,index=True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))


    #指定外键
    users = db.relationship('User',backref='role')
    def __repr__(self):
        return '<Role %r>' % self.name
class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),unique=True,index=True)
    email = db.Column(db.String(128),unique=True,index=True)
    password = db.Column(db.String(128))

    confirmed = db.Column(db.Boolean,default=False)
    #关于外键的设置
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))

    # 实现密码散列
    password_hash = db.Column(db.String(128))
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)
    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return '<User %r>' % self.username

    def generate_confirmation_token(self,expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'],expiration)
        return s.dumps({'confirm':self.id})
    def confirm(self,token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

#登陆认证
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

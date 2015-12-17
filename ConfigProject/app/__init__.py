# -*- coding: utf-8 -*-
#! /usr/bin/env python
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
# from flask_wtf.csrf import CsrfProtect

from config import config


bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
# csrf = CsrfProtect()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'


def create_app(config_name):
    app = Flask(__name__)
    #配置文件初始化
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    #前段页面模版引擎初始化
    bootstrap.init_app(app)
    #邮箱初始化
    mail.init_app(app)
    #本地化时间初始化
    moment.init_app(app)
    #数据库初始化
    db.init_app(app)

    #蓝图注册
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint,url_prefix='')

    #登陆认证初始化
    login_manager.init_app(app)

    #CSRC保护初始化
    # csrf.init_app(app)

    return app


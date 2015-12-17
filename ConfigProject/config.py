# -*- coding: utf-8 -*-
#! /usr/bin/env python
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'liweiCDK'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASK_MAIL_SUBJECT_PREFIX = '[ConfigProject]'
    FLASK_MAIL_SENDER = 'liweijavakf@163.com'
    FLASK_ADMIN = 'liwei'

    @staticmethod
    def init_app(app):
        pass
class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'liweijavakf@163.com'
    MAIL_PASSWORD = 'liwei429'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@127.0.0.1/flask'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@127.0.0.1/flask'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@127.0.0.1/flask'

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,

}

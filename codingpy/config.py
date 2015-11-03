#!usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
from logging.handlers import RotatingFileHandler

basedir = os.path.abspath(os.path.dirname(__file__))
datadir = 'data'


class Config:
    SITE_NAME = 'codingpy | 编程派'
    SECRET_KEY = os.urandom(32)
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    # 是否启用博客模式
    # BLOG_MODE = True

    # html or markdown
    BODY_FORMAT = os.getenv('BODY_FORMAT')  # or 'html'

    # mail setup
    MAIL_SERVER = 'smtp.126.com'
    MAIL_PORT = 25
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_SUBJECT_PREFIX = '[CODINGPY]'
    MAIL_SENDER = 'CODINGPY Admin <codingpy@126.com>'

    APP_ADMIN = os.environ.get('CODINGPY_ADMIN')

    # flask-cache configuration
    CACHE_KEY = 'view/%s'  # ?
    CACHE_DEFAULT_TIMEOUT = 30
    # 使用uwsgi_cache效果更好
    CACHE_TYPE = 'redis'
    CACHE_REDIS_HOST = 'localhost'
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_URL = 'redis://localhost:6379'

    # QiNiu Cloud Storage
    QINIU_AK = os.getenv('QINIU_AK') or ''
    QINIU_SK = os.getenv('QINIU_SK') or ''
    QINIU_BUCKET = os.getenv('QINIU_BUCKET') or ''
    QINIU_DOMAIN = os.getenv('QINIU_DOMAIN') or '%s.qiniudn.com' % QINIU_BUCKET

    @staticmethod
    def init_app(app):
        _handler = RotatingFileHandler(
            'app.log', maxBytes=10000, backupCount=1)
        _handler.setLevel(logging.WARNING)
        app.logger.addHandler(_handler)

        # TODO
        # mail_handler = Config.get_mailhandler()
        # app.logger.addHandler(mail_handler)


class DevelopmentConfig(Config):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI') \
        or "postgresql://vagrant:vagrant@localhost/codingpy" or \
        'sqlite:///%s' % os.path.join(basedir, 'data_dev_sqlite.db')

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


class ProductionConfig(Config):
    # CACHE_DIR = os.path.join(basedir, datadir, 'cache')
    DEBUG = False

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
        "postgresql://earlgrey:earlgrey@localhost/codingpy"

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


class TestingConfig(Config):
    TESTING = True

    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URI') or \
        'sqlite:///:memory:'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}

#!usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging

basedir = os.path.abspath(os.path.dirname(__file__))
datadir = 'data'


class Config:
    SITE_NAME = 'codingpy'
    SECRETE_KEY = os.urandom(32)

    # mail setup
    MAIL_SERVER = 'smtp.126.com'
    MAIL_PORT = 25
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_SUBJECT_PREFIX = '[CODINGPY]'
    MAIL_SENDER = 'CODINGPY Admin <songbingjin@126.com>'

    ADMIN = os.environ.get('CODINGPY_ADMIN')

    # flask-cache configuration
    CACHE_KEY = 'codingpy/%s'
    CACHE_DEFAULT_TIMEOUT = 300

    # QiNiu Cloud Storage
    QINIU_AK = os.getenv('QINIU_AK') or ''
    QINIU_SK = os.getenv('QINIU_SK') or ''
    QINIU_BUCKET = os.getenv('QINIU_BUCKET') or ''
    QINIU_DOMAIN = os.getenv('QINIU_DOMAIN') or '%s.qiniudn.com' % QINIU_BUCKET

    @staticmethod
    def init_app(app):
        _handler = logging.StreamHandler()
        app.logger.addHandler(_handler)

        # TODO
        # mail_handler = Config.get_mailhandler()
        # app.logger.addHandler(mail_handler)


class DevelopmentConfig(Config):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI') \
        or "postgresql:///postgres@localhost/codingpy" or \
        'sqlite:///%s' % os.path.join(basedir, 'data_dev_sqlite.db')

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


class ProductionConfig(Config):
    CACHE_TYPE = 'filesystem'
    CACHE_DIR = os.path.join(basedir, datadir, 'cache')

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')

    # postgresql configuration
    POSTGRES_USER = os.getenv('POSTGRES_USER') or ''
    POSTGRES_PASS = os.getenv('POSTGRES_PASS') or ''
    POSTGRES_HOST = os.getenv('POSTGRES_HOST') or ''
    POSTGRES_PORT = os.getenv('POSTGRES_PORT') or ''
    POSTGRES_DB = os.getenv('POSTGRES_DB') or ''

    if (len(POSTGRES_USER) > 0 and len(POSTGRES_PASS) > 0 and
            len(POSTGRES_HOST) > 0 and len(POSTGRES_PORT) > 0 and
            len(POSTGRES_DB) > 0):
        SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI') or \
            'postgresql://%s:%s@%s:%s/%s' % (
                POSTGRES_USER, POSTGRES_PASS, POSTGRES_HOST,
                POSTGRES_PORT, POSTGRES_DB)

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # mail_handler = Config.get_mailhandler()
        # app.logger.addHandler(mail_handler)


class TestingConfig(Config):
    TESTING = True

    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URI') or \
        'sqlite:///:memory:'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

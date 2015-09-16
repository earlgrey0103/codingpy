#!usr/bin/env python
# -*- coding: utf-8 -*-

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRETE_KEY = os.urandom(32)
    MAIL_SUBJECT_PREFIX = '[CODINGPY]'
    MAIL_SENDER = 'CODINGPY Admin <songbingjin@126.com>'
    ADMIN = os.environ.get('CODINGPY_ADMIN')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.126.com'
    MAIL_PORT = 25
    MAIL_USERNAME = os.environ.get('DEV_MAIL')
    MAIL_PASSWORD = os.environ.get('DEV_MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI') \
        or "postgresql://postgres@localhost/codingpy"


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('PRO_DATABASE_URI')


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URI')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

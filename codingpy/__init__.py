#!usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

from flask import Flask, render_template, g, request
from flask.ext.bootstrap import Bootstrap
from flask.ext.mail import Mail, Message
from flask.ext.moment import Moment
from flask.ext.login import LoginManager, current_user, logout_user
from flask_wtf.csrf import CsrfProtect

# 将project目录加入sys.path
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_path not in sys.path:
    sys.path.insert(0, project_path)

csrf = CsrfProtect()

bootstrap = Bootstrap()
moment = Moment()
mail = Mail()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    csrf.init_app(app)

    register_db(app)
    register_login_manager(app)
    register_routes(app)
    register_uploadsets(app)
    register_error_handle(app)

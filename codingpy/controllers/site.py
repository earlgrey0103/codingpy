#!usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint
from flask import render_template, redirect, url_for, flash, request,\
    current_app
from werkzeug.contrib.atom import AtomFeed

# from ..models import Permission
from ..ext import cache
from ..models import Article

bp = Blueprint('site', __name__)


# @bp.app_context_processor
# def inject_permissions():
#     return dict(Permission=Permission)


@bp.route('/')
@cache.cached()
def index():
    article = Article.query.first()

    return render_template('index.html', a=article)


@bp.route('/article/')
@cache.cached()
def article():
    return render_template('article.html')


@bp.route('/login/')
@cache.cached()
def login():
    return render_template('login.html')


@bp.route('/register/')
@cache.cached()
def register():
    return render_template('register.html')

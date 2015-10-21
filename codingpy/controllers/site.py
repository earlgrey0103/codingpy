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
@bp.route('/index/')
@cache.cached()
def index():
    # Latest articles
    latest_articles = Article.query.filter(Article.published == True).\
        order_by(Article.created_at.desc()).limit(5)

    return render_template('index.html', latest_articles=latest_articles)


@bp.route('/<article_slug>/')
@cache.cached()
def article(article_slug):
    article = Article.query.filter(Article.slug == article_slug).first()
    return render_template('article.html', article=article)


@bp.route('/<category>/')
@cache.cached()
def category(category):
    pass


@bp.route('/tag/<tag_name>/')
@cache.cached()
def tag(tag_name):
    pass


@bp.route('/feed/')
@cache.cached()
def feed():
    pass

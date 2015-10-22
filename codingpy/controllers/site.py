#!usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint
from flask import render_template, redirect, url_for, flash, request,\
    current_app, jsonify
from werkzeug.contrib.atom import AtomFeed

# from ..models import Permission
from ..ext import cache
from ..models import Article, Tag

bp = Blueprint('site', __name__)


# @bp.app_context_processor
# def inject_permissions():
#     return dict(Permission=Permission)


@bp.route('/')
@bp.route('/index/')
@cache.cached()
def index():
    # Latest 10 articles
    latest_articles = Article.query.filter(Article.published == True).\
        order_by(Article.created_at.desc()).limit(5)

    # Tags
    tags = Tag.query.order_by(Tag.hits.desc()).all()

    return render_template('index.html',
                           latest_articles=latest_articles,
                           tags=tags)


@bp.route('/load_more/', methods=['GET'])
def load_more():
    start_article_id = 1
    next_ten_articles = Article.query.filter(
        start_article_id <= Article.id,
        Article.id <= start_article_id + 0).all()

    # build a dict of new articles
    send_dict = {}

    for article in next_ten_articles:
        send_dict[article.title] = {'article_slug': article.slug,
                                    'article.id': article.id,
                                    'article.summary': article.summary, }

    return jsonify(send_dict)


@bp.route('/<article_slug>/')
@cache.cached()
def article(article_slug):
    article = Article.query.filter(Article.slug == article_slug).first()
    return render_template('article.html', article=article)


@bp.route('/<category>/')
@cache.cached()
def category(category):
    pass


@bp.route('/tag/<name>/')
@cache.cached()
def tag(name):
    pass


@bp.route('/feed/')
@cache.cached()
def feed():
    pass

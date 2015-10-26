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

    category_label = """
    <a class="ui red ribbon label" href="%s">
    <i class="book icon"></i>%s</a>

    """

    header = """
    <div class="header">
    <a href="%s">
    <h2>%s</h2>
    </a></div>
    """

    image = """
    <div class="image ">
        <div class="article-thumb" data-bg=" %s ">
        </div>
    </div>
    """

    summary = """
    <div class="article-content">
        <div class="description">
            %s
        </div>
    </div>
    """

    feed = """%s """
    for article in next_ten_articles:
        html = (category_label + header + image + summary + feed) %\
            (article.category.name,
             article.category.name,
             article.title, article.title,
             url_for('static', filename=article.thumbnail),
             article.summary,
             article.created_at)
        send_dict[article.title] = html

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

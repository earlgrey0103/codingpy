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
@bp.route('/page/<int:page>')
@cache.cached()
def index(page=1):
    _base_query = Article.query.public()
    # Latest 10 articles
    template_name = 'index.html' if page == 1 else 'items.html'
    all_articles = _base_query.order_by(Article.created_at.desc()).\
        paginate(page, Article.PER_PAGE, False).items

    # Tags
    tags = Tag.query.order_by(Tag.hits.desc()).all()

    # recommended articles top 5
    recommended_articles = _base_query.filter_by(recommended=True).limit(5)
    popular_articles = _base_query.\
        order_by(Article.hits.desc()).limit(5)

    from sqlalchemy.sql.expression import func
    random_articles = _base_query.order_by(func.random()).limit(5)

    return render_template(template_name,
                           all_articles=all_articles,
                           recommended_articles=recommended_articles,
                           popular_articles=popular_articles,
                           random_articles=random_articles,
                           tags=tags,
                           page=page)


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

#!usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint
from flask import render_template, redirect, url_for, flash, request,\
    current_app, jsonify
from werkzeug.contrib.atom import AtomFeed

# from ..models import Permission
from ..ext import cache
from ..models import Article, Tag, Category, db

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
    tags = Tag.query.order_by(Tag.hits.desc()).limit(10)

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


@bp.route('/article/<article_slug>/')
@cache.cached()
def article(article_slug):
    article = Article.query.filter(Article.slug == article_slug).first()
    article.hits += 1

    db.session.add(article)
    db.session.commit()

    related_articles = Article.query.search(article.keywords).limit(3)

    _base_query = Article.query.public()

    # Tags
    tags = Tag.query.order_by(Tag.hits.desc()).limit(10)

    # recommended articles top 5
    recommended_articles = _base_query.filter_by(recommended=True).limit(5)
    popular_articles = _base_query.\
        order_by(Article.hits.desc()).limit(5)

    from sqlalchemy.sql.expression import func
    random_articles = _base_query.order_by(func.random()).limit(5)

    return render_template('article.html',
                           article=article,
                           tags=tags,
                           related_articles=related_articles,
                           recommended_articles=recommended_articles,
                           popular_articles=popular_articles,
                           random_articles=random_articles)


@bp.route('/category/<slug>/')
@bp.route('/category/page/<int:page>')
@cache.cached()
def category(slug, page=1):
    category = Category.query.filter_by(slug=slug).first()
    _base_query = Article.query.public().filter_by(category=category)

    all_articles = _base_query.order_by(Article.created_at.desc()).\
        paginate(page, Article.PER_PAGE, False).items

    # Tags
    tags = Tag.query.order_by(Tag.hits.desc()).limit(10)

    # recommended articles top 5
    recommended_articles = _base_query.filter_by(recommended=True).limit(5)
    popular_articles = _base_query.\
        order_by(Article.hits.desc()).limit(5)

    from sqlalchemy.sql.expression import func
    random_articles = _base_query.order_by(func.random()).limit(5)

    return render_template('index.html',
                           page=page,
                           tags=tags,
                           category=category,
                           all_articles=all_articles,
                           recommended_articles=recommended_articles,
                           popular_articles=popular_articles,
                           random_articles=random_articles)


# not implemented for now
@bp.route('/tag/<name>/')
@cache.cached()
def tag(name):
    pass


@bp.route('/feed/')
@cache.cached()
def feed():
    pass

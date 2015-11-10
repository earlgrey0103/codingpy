#!usr/bin/env python
# -*- coding: utf-8 -*-
import datetime

from flask import Blueprint, abort
from flask import render_template, redirect, url_for, flash, request,\
    current_app, jsonify, make_response
from werkzeug.contrib.atom import AtomFeed, FeedEntry

# from ..models import Permission
from ..ext import cache
from ..models import Article, Tag, Category, db

bp = Blueprint('site', __name__)


# @bp.app_context_processor
# def inject_permissions():
#     return dict(Permission=Permission)


@bp.route('/')
@bp.route('/index/')
@bp.route('/page/<int:page>/')
@cache.cached()
def index(page=1):
    _base_query = Article.query.public()
    # Latest 10 articles
    template_name = 'index.html' if page == 1 else 'includes/items.html'
    all_articles = _base_query.order_by(Article.created_at.desc()).\
        paginate(page, Article.PER_PAGE, False).items

    # Tags
    tags = Tag.query.order_by(Tag.views.desc()).limit(10)

    slides = _base_query.filter_by(slider=True).order_by(
        Article.created_at.desc()).limit(5)

    # recommended articles top 5
    recommended_articles = _base_query.filter_by(recommended=True).limit(5)
    popular_articles = _base_query.\
        order_by(Article.views.desc()).limit(5)

    from sqlalchemy.sql.expression import func
    random_articles = _base_query.order_by(func.random()).limit(5)

    return render_template(template_name,
                           all_articles=all_articles,
                           recommended_articles=recommended_articles,
                           popular_articles=popular_articles,
                           random_articles=random_articles,
                           slides=slides,
                           tags=tags,
                           page=page)


@bp.route('/article/<article_slug>/')
@cache.cached()
def article(article_slug):
    article = Article.query.filter(Article.slug == article_slug).first()
    if not article.published:
        abort(403)

    article.views += 1

    db.session.add(article)
    db.session.commit()

    related_articles = Article.query.search(article.keywords).\
        filter(Article.id != article.id).limit(3)

    _base_query = Article.query.public()

    # Tags
    tags = Tag.query.order_by(Tag.views.desc()).limit(10)

    # recommended articles top 5
    recommended_articles = _base_query.filter_by(recommended=True).limit(5)
    popular_articles = _base_query.\
        order_by(Article.views.desc()).limit(5)

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
    tags = Tag.query.order_by(Tag.views.desc()).limit(10)

    # recommended articles top 5
    recommended_articles = _base_query.filter_by(recommended=True).limit(5)
    popular_articles = _base_query.\
        order_by(Article.views.desc()).limit(5)

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


@bp.route('/tag/<slug>/')
@bp.route('/tag/page/<int:page>')
@cache.cached()
def tag(slug, page=1):
    tag = Tag.query.filter_by(slug=slug).first()
    _base_query = Article.query.public().filter(
        Article.tags.any(id=tag.id))

    all_articles = _base_query.order_by(Article.created_at.desc()).\
        paginate(page, Article.PER_PAGE, False).items

    # Tags
    tags = Tag.query.order_by(Tag.views.desc()).limit(10)

    # recommended articles top 5
    recommended_articles = _base_query.filter_by(recommended=True).limit(5)
    popular_articles = _base_query.\
        order_by(Article.views.desc()).limit(5)

    from sqlalchemy.sql.expression import func
    random_articles = _base_query.order_by(func.random()).limit(5)

    return render_template('index.html',
                           page=page,
                           tags=tags,
                           tag=tag,
                           all_articles=all_articles,
                           recommended_articles=recommended_articles,
                           popular_articles=popular_articles,
                           random_articles=random_articles)


@bp.route('/sitemap.xsl/')
def sitemap_xsl():
    response = make_response(render_template('sitemap.xsl'))
    response.mimetype = 'text/atom+xsl'
    return response


@bp.route('/sitemap.xml/', methods=['GET'])
def sitemap_xml():
    """Generate sitemap.xml. Makes a list of urls and date modified."""
    urlset = []

    urlset.append(dict(
        loc=url_for('site.index', _external=True),
        lastmod=datetime.date.today().isoformat(),
        changefreq='weekly',
        priority=1,
    ))

    # categories
    categories = Category.query.all()

    for category in categories:
        urlset.append(dict(
            loc=category.link,
            changefreq='weekly',
            priority=0.8,
        ))

    # tags
    # tags = Tag.query.all()

    # for tag in tags:
    #     urlset.append(dict(
    #         loc=tag.link,
    #         changefreq='weekly',
    #         priority=0.6,
    #     ))

    # articles model pages
    articles = Article.query.public().all()

    for article in articles:
        url = article.link
        modified_time = article.last_modified.date().isoformat()
        urlset.append(dict(
            loc=url,
            lastmod=modified_time,
            changefreq='monthly',
            priority=0.5,
        ))

    sitemap_xml = render_template('sitemap.xml', urlset=urlset)
    res = make_response(sitemap_xml)
    res.headers['Content-type'] = 'application/xml; charset=utf-8'
    return res


def _generate_entry(article):
    return FeedEntry(article.title,
                     url=article.link,
                     updated=article.last_modified,
                     published=article.created_at,
                     content=article.body_html,
                     summary=article.summary or '')


# 不能开启cache，否则导致浏览器无法解析xml文件
@bp.route('/feed/')
def feed():
    site_name = '编程派'

    feed = AtomFeed(
        "%s 最新文章" % site_name,
        feed_url=request.url,
        url=request.url_root,
    )

    articles = Article.query.public().limit(10).all()

    for article in articles:
        entry = _generate_entry(article)
        feed.add(entry)

    res = make_response(render_template('rssfeed.xml', articles=articles))
    res.headers['Content-type'] = 'application/xml; charset=utf-8'
    return res

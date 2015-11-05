#!usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
import os.path as op

from flask import flash, redirect, url_for, request
from flask.ext.login import current_user, login_required
from flask.ext.admin import Admin, AdminIndexView, expose
# from flask.ext.login import current_user
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
from flask.ext.admin.actions import action
from flask_admin.form import ImageUploadField

from .models import Article, User, Category, Tag, Topic, db
from .ext import cache
from .config import Config
from .utils.helpers import baidu_ping, notify_baidu
from .decorators import admin_required

file_path = op.join(op.dirname(__file__), 'static')
cache_key = Config.CACHE_KEY


def cache_delete(key):
    keys = [cache_key % key]
    for _key in keys:
        cache.delete(_key)


class CodingpyAdmin(AdminIndexView):

    @expose('/')
    @login_required
    @admin_required
    def index(self):
        latest_articles = Article.query.\
            order_by(Article.created_at.desc()).limit(5)

        return self.render('admin/index.html', latest_articles=latest_articles)

    def is_accessible(self):
        return current_user.is_administrator()

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('account.login', next=request.url))


class ArticleAdmin(ModelView):

    @expose('/<article_id>/')
    def preview(self, article_id):
        article = Article.query.get_or_404(article_id)
        return self.render('article.html', article=article)

    create_template = "admin/a_create.html"
    edit_template = "admin/a_edit.html"

    column_list = ('title', 'category', 'published', 'ontop',
                   'recommended', 'created_at', 'views')

    form_excluded_columns = ('author', 'body_html', 'views', 'created_at',
                             'last_modified', 'template', 'comments')

    column_searchable_list = ('title',)

    form_overrides = dict(
        thumbnail=ImageUploadField,
        thumbnail_big=ImageUploadField)

    form_args = {
        'thumbnail': {
            'label': '缩略图',
            'base_path': file_path,
            'allow_overwrite': True,
            'relative_path': 'thumbnails/',
        },
        'thumbnail_big': {
            'label': '大缩略图',
            'base_path': file_path,
            'allow_overwrite': True,
            'relative_path': 'thumbnails/',
        },

    }

    column_labels = dict(
        title=('标题'),
        slug=('URL Slug'),
        seotitle=('SEO 标题'),
        category=('类别'),
        topic=('专题'),
        tags=('标签'),
        body=('正文'),
        summary=('摘要'),
        published=('发布'),
        ontop=('置顶'),
        recommended=('推荐'),
        seokey=('SEO 关键词'),
        seodesc=('SEO 描述'),
        thumbnail=('缩略图'),
        thumbnail_big=('大缩略图'),
        template=('模板'),
        created_at=('创建时间'),
        views=('阅读数'),
        keywords=('关键词'),
        source=('来源'),
        slider=('轮播'),
    )

    form_widget_args = {
        'title': {'style': 'width:320px;'},
        'category': {'style': 'width:320px;'},
        'topic': {'style': 'width:320px;'},
        'tags': {'style': 'width:320px;'},
        'keywords': {'style': 'width:320px;'},
        'source': {'style': 'width:320px;'},
        'slug': {'style': 'width:320px;'},
        'seotitle': {'style': 'width:320px;'},
        'seokey': {'style': 'width:320px;'},
        'seodesc': {'style': 'width:320px; height:80px;'},
        'thumbnail': {'style': 'width:320px;'},
        'thumbnail_big': {'style': 'width:320px;'},
        'summary': {'style': 'width:680px; height:80px;'},
        'body': {'style': 'width:680px; height:240px;'},
        'published': {'class': 'col-md-1'},
        'ontop': {'class': 'col-md-1'},
        'recommended': {'class': 'col-md-1'},
        'slider': {'class': 'col-md-1'},
    }

    # Model handlers
    def on_model_change(self, form, model, is_created):
        if is_created:
            model.author_id = current_user.id
            model.created_at = datetime.now()
            model.last_modified = model.created_at
        else:
            model.last_modified = datetime.now()

    def after_model_change(self, form, model, is_created):
        # 如果发布新文章，则PING通知百度
        site = "http://www.codingpy.com"
        link = site + model.shortlink
        # 由于使用了Nginx反向代理, model.link的域名部分是localhost
        if is_created and model.published:
            baidu_ping(link)
            notify_baidu(link)

        # 清除缓存，以便可以看到最新内容
        cache_delete(model.shortlink)

    @action('pingbaidu', 'Ping to Baidu')
    def action_ping_baidu(self, ids):
        for id in ids:
            obj = Article.query.get(id)
            site = "http://www.codingpy.com"
            link = site + obj.shortlink
            baidu_ping(link)
            notify_baidu(link)
        flash(u'PING请求已发送，请等待百度处理')


class CategoryAdmin(ModelView):

    # create_template = "admin/model/a_create.html"
    # edit_template = "admin/model/a_edit.html"

    column_list = ('name', 'slug', 'seotitle', 'views')

    column_searchable_list = ('slug', 'longslug', 'name')

    form_excluded_columns = ('articles', 'body_html', 'longslug', 'children',
                             'body', 'template', 'article_template', 'views')

    # form_overrides = dict(seodesc=TextAreaField, body=EDITOR_WIDGET)

    column_labels = dict(
        parent=('父栏目'),
        slug=('URL Slug'),
        name=('名称'),
        seotitle=('SEO 名称'),
        body=('正文'),
        seokey=('SEO 关键词'),
        seodesc=('SEO 描述'),
        thumbnail=('缩略图'),
        views=('阅读数'),
        icon=('图标')
    )

    form_widget_args = {
        'parent': {'style': 'width:320px;'},
        'slug': {'style': 'width:320px;'},
        'name': {'style': 'width:320px;'},
        'icon': {'style': 'width:320px;'},
        'thumbnail': {'style': 'width:320px;'},
        'seotitle': {'style': 'width:320px;'},
        'seokey': {'style': 'width:320px;'},
        'seodesc': {'style': 'width:320px; height:80px;'},
    }

    form_overrides = dict(thumbnail=ImageUploadField)
    form_args = {
        'thumbnail': {
            'label': '缩略图',
            'base_path': file_path,
            'allow_overwrite': True,
            'relative_path': 'thumbnails/',
        }
    }


class UserAdmin(ModelView):

    column_list = ('email', 'username', 'name', 'role',
                   'confirmed', 'last_seen')

    form_excluded_columns = (
        'password_hash', 'avatar_hash', 'articles', 'member_since',
        'last_seen', 'comments')

    column_searchable_list = ('email', 'username', 'name')

    column_labels = dict(
        email=('邮箱'),
        username=('用户名'),
        name=('昵称'),
        confirmed=('已确认'),
        about_me=('简介'),
        role=('角色'),
    )

    form_widget_args = {
        'about_me': {'style': 'width:320px;'},
        'email': {'style': 'width:320px;'},
        'username': {'style': 'width:320px;'},
        'name': {'style': 'width:320px;'},
        'confirmed': {'class': 'col-md-1'},
        'role': {'style': 'width:320px;'},
    }


class TagAdmin(ModelView):

    # create_template = "admin/a_create.html"
    # edit_template = "admin/a_edit.html"

    column_list = ('name', 'seotitle', 'seokey', 'views')

    column_searchable_list = ('name',)

    form_excluded_columns = ('articles', 'body_html', 'template', 'views')

    form_overrides = dict(thumbnail=ImageUploadField)

    form_args = {
        'thumbnail': {
            'label': '缩略图',
            'base_path': file_path,
            'allow_overwrite': True,
            'relative_path': 'thumbnails/',
        },
    }

    column_labels = dict(
        slug=('URL Slug'),
        name=('名称'),
        seotitle=('SEO 名称'),
        body=('正文'),
        seokey=('SEO 关键词'),
        seodesc=('SEO 描述'),
        thumbnail=('缩略图'),
        views=('阅读数'),
    )

    form_widget_args = {
        'slug': {'style': 'width:320px;'},
        'name': {'style': 'width:320px;'},
        'thumbnail': {'style': 'width:320px;'},
        'seotitle': {'style': 'width:320px;'},
        'seokey': {'style': 'width:320px;'},
        'seodesc': {'style': 'width:320px; height:80px;'},
        'body': {'style': 'width:320px; height:80px;'},
    }


class TopicAdmin(ModelView):

    create_template = "admin/a_create.html"
    edit_template = "admin/a_edit.html"

    column_list = ('name', 'slug', 'seotitle')

    form_excluded_columns = ('articles', 'body_html', 'views')

    column_searchable_list = ('slug', 'name')

    column_labels = dict(
        slug=('URL Slug'),
        name=('名称'),
        seotitle=('SEO 名称'),
        body=('正文'),
        seokey=('SEO 关键词'),
        seodesc=('SEO 描述'),
        thumbnail=('缩略图'),
        template=('模板'),
    )

    form_widget_args = {
        'slug': {'style': 'width:320px;'},
        'name': {'style': 'width:320px;'},
        'thumbnail': {'style': 'width:320px;'},
        'seotitle': {'style': 'width:320px;'},
        'seokey': {'style': 'width:320px;'},
        'seodesc': {'style': 'width:320px; height:80px;'},
        'template': {'style': 'width:320px;'},
    }


admin = Admin(index_view=CodingpyAdmin(name='首页'),
              name='编程派',
              template_mode='bootstrap3')

admin.add_view(ArticleAdmin(Article, db.session, name='文章'))
admin.add_view(CategoryAdmin(Category, db.session, name='分类'))
admin.add_view(UserAdmin(User, db.session, name='用户'))
admin.add_view(TagAdmin(Tag, db.session, name='标签'))
admin.add_view(TopicAdmin(Topic, db.session, name='专题'))
admin.add_view(FileAdmin(file_path, '/static/', name='文件'))

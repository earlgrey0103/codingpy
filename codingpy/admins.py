#!usr/bin/env python
# -*- coding: utf-8 -*-

# from flask import redirect, url_for, request
from flask.ext.admin import Admin, AdminIndexView, expose
# from flask.ext.login import current_user
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin.form import ImageUploadField

from .models import Article, User, Category, Tag, Topic, db

import os.path as op

file_path = op.join(op.dirname(__file__), 'static')


class CodingpyAdmin(AdminIndexView):

    @expose('/')
    def index(self):
        latest_articles = Article.query.\
            order_by(Article.created_at.desc()).limit(5)

        return self.render('admin/index.html', latest_articles=latest_articles)

    # def is_accessible(self):
    #     return current_user.is_administrator()

    # def inaccessible_callback(self, name, **kwargs):
    #     # redirect to login page if user doesn't have access
    #     return redirect(url_for('site.login', next=request.url))


class ArticleAdmin(ModelView):

    @expose('/<article_id>/')
    def preview(self, article_id):
        article = Article.query.get_or_404(article_id)
        return self.render('article.html', article=article)

    create_template = "admin/a_create.html"
    edit_template = "admin/a_edit.html"

    column_list = ('title', 'category', 'tags', 'published', 'ontop',
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
        'published': {'class': 'col-md-1'},
        'ontop': {'class': 'col-md-1'},
        'recommended': {'class': 'col-md-1'},
        'slider': {'class': 'col-md-1'},
    }


class CategoryAdmin(ModelView):

    # create_template = "admin/model/a_create.html"
    # edit_template = "admin/model/a_edit.html"

    column_list = ('name', 'slug', 'seotitle', 'views')

    column_searchable_list = ('slug', 'longslug', 'name')

    form_excluded_columns = ('articles', 'body_html', 'longslug', 'children',
                             'body', 'template', 'article_template', 'views')

    # form_overrides = dict(seodesc=TextAreaField, body=EDITOR_WIDGET)

    # column_formatters = dict(view_on_site=view_on_site)

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


class UserAdmin(ModelView):

    column_list = ('email', 'username', 'name', 'role', 'confirmed')

    form_excluded_columns = (
        'password_hash', 'avatar_hash', 'articles', 'member_since',
        'last_seen')

    column_searchable_list = ('email', 'username', 'name')

    # form_overrides = dict(about_me=TextAreaField)

    column_labels = dict(
        email=('邮箱'),
        username=('用户名'),
        name=('昵称'),
        confirmed=('已确认'),
        about_me=('简介'),
        role=('角色'),
    )

    form_widget_args = {
        'about_me': {'style': 'width:320px; height:80px;'},
    }


class TagAdmin(ModelView):

    # create_template = "admin/a_create.html"
    # edit_template = "admin/a_edit.html"

    column_list = ('name', 'seotitle', 'seokey', 'views')

    column_searchable_list = ('name',)

    form_excluded_columns = ('articles', 'body_html')

    # form_overrides = dict(seodesc=TextAreaField, body=EDITOR_WIDGET)

    # column_formatters = dict(view_on_site=view_on_site)

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

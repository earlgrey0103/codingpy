#!usr/bin/env python
# -*- coding: utf-8 -*-

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from .models import Article, User, Role, Category, db

admin = Admin()


# class CodingpyModelView(ModelView):

#     def is_accessible(self):
#         return current_user.is_authenticated()

#     def inaccessible_callback(self, name, **kwargs):
#         # redirect to login page if user doesn't have access
#         return redirect(url_for('site.login', next=request.url))

# Customized Post model admin

class ArticleAdmin(ModelView):

    column_list = ('title', 'category', 'tags', 'published', 'ontop',
                   'recommend', 'created', 'view_on_site')

    form_excluded_columns = ('author', 'body_html', 'hits', 'created',
                             'last_modified',)

    column_searchable_list = ('title',)

    # form_create_rules = (
    #     'title', 'seotitle', 'category', 'topic', 'tags', 'body',
    #     'summary', 'published', 'ontop', 'recommend', 'seokey',
    #     'seodesc', 'thumbnail', 'thumbnail_big', 'template',
    # )
    # form_edit_rules = form_create_rules

# form_overrides = dict(seodesc=TextAreaField, body=EDITOR_WIDGET,
#                       summary=TextAreaField)

    column_labels = dict(
        title=('标题'),
        seotitle=('SEO 标题'),
        category=('类别'),
        topic=('专题'),
        tags=('标签'),
        body=('正文'),
        summary=('摘要'),
        published=('发布'),
        ontop=('置顶'),
        recommend=('推荐'),
        seokey=('SEO 关键词'),
        seodesc=('SEO 描述'),
        thumbnail=('缩略图'),
        thumbnail_big=('大缩略图'),
        template=('模板'),
        created=('创建时间'),
        view_on_site=('阅读数'),
    )

    # form_widget_args = {
    #     'title': {'style': 'width:480px;'},
    #     'slug': {'style': 'width:480px;'},
    #     'seotitle': {'style': 'width:480px;'},
    #     'seokey': {'style': 'width:480px;'},
    #     'seodesc': {'style': 'width:480px; height:80px;'},
    #     'thumbnail': {'style': 'width:480px;'},
    #     'thumbnail_big': {'style': 'width:480px;'},
    #     'template': {'style': 'width:480px;'},
    #     'summary': {'style': 'width:680px; height:80px;'},
    # }


admin.add_view(ModelView(User, db.session))
admin.add_view(ArticleAdmin(Article, db.session))
admin.add_view(ModelView(Role, db.session))
admin.add_view(ModelView(Category, db.session))

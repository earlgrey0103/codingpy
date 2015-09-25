#!usr/bin/env python
# -*- coding: utf-8 -*-

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from .models import Article, User, Role, Category, db

admin = Admin()

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Article, db.session))
admin.add_view(ModelView(Role, db.session))
admin.add_view(ModelView(Category, db.session))

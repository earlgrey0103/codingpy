#!usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint
from flask import render_template, redirect, url_for, flash, request,\
    current_app
from werkzeug.contrib.atom import AtomFeed

# from ..models import Permission
from ..ext import cache

bp = Blueprint('site', __name__)


# @bp.app_context_processor
# def inject_permissions():
#     return dict(Permission=Permission)


@bp.route('/')
@cache.cached()
def index():
	return render_template('index.html')

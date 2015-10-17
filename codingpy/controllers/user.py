#!usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint
from flask import render_template, redirect, url_for, flash, request,\
    current_app

bp = Blueprint('user', __name__)


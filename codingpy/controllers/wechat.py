#!usr/bin/env python
# -*- coding: utf-8 -*-

"""
Wechat Auto Replies.

:copyright: (c) 2016 by EarlGrey.

"""

import os
# import time
import hashlib

from flask import Blueprint, request, make_response


# from ..ext import db
# from ..models import User
# from ..forms import LoginForm, RegistrationForm

bp = Blueprint('wechat', __name__)


@bp.route('/', methods=['GET', 'POST'])
def wechat_auth():
    """Authenticate reply is from wechat official server."""
    if request.method == 'GET':
        token = os.getenv('wechat_token')  # your token
        query = request.args  # GET 方法附上的参数
        signature = query.get('signature', '')
        timestamp = query.get('timestamp', '')
        nonce = query.get('nonce', '')
        echostr = query.get('echostr', '')
        s = [timestamp, nonce, token]
        s.sort()
        s = ''.join(s)
        if (hashlib.sha1(s).hexdigest() == signature):
            return make_response(echostr)
    else:
        # process post messages from wechat
        pass

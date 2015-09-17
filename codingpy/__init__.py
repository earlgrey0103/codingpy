#!usr/bin/env python
# -*- coding: utf-8 -*-

from ._base import *
from .models import *
from .ext import *

__all__ = [_base.__all__, models.__all__, ext.__all__]


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

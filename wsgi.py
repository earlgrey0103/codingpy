#!usr/bin/env python
# -*- coding: utf-8 -*-

from gevent.wsgi import WSGIServer
import logging
from logging.handlers import RotatingFileHandler

from manage import app as application

application.jinja_env.cache = {}

if __name__ == '__main__':
    formatter = logging.Formatter(
        "[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
    handler = RotatingFileHandler(
        'codingpy.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.WARNING)
    handler.setFormatter(formatter)
    application.logger.addHandler(handler)

    http_server = WSGIServer(('', 5000), application)
    http_server.serve_forever()

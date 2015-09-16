#!usr/bin/env python
# -*- coding: utf-8 -*-
import os
# import sys


from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from codingpy import create_app, db

app = create_app(os.getenv('APP_CONFIG') or 'default')

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


@manager.shell
def make_shell_context():
    from codingpy.models import User, Role, Permission, Category,\
        Tag, Article, Topic, Label
    return dict(
        app=app, db=db, User=User, Role=Role, Permission=Permission,
        Category=Category, Tag=Tag, Article=Article, Topic=Topic,
        Label=Label
    )


@manager.add_command
def test(coverage=False):
    """Run unit tests and/or covrage reports
    """
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':
    manager.run()

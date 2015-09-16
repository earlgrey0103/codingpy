#!usr/bin/env python
# -*- coding: utf-8 -*-

from flask.ext.script import Manager
from flask.ext.mail import Mail, Message
from flask.ext.migrate import Migrate, MigrateCommand

from codingpy import app, db

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
	manager.run()
# -*- coding: utf-8 -*-

import os
import time
import random
import datetime
from flask import current_app, url_for


class SaveUploadFile(object):
    """文件上传到去云存储"""

    def __init__(self, fext, data):
        # 图片文件自动生成文件名
        # 非图片文件使用原文件名
        if fext.startswith('.'):
            self.filename = u'%s/%s%s' % (self.gen_dirname(),
                                          self.gen_filename(), fext)
        else:
            self.filename = u'%s/%s' % (self.gen_dirname(), fext)
        self.data = data

    def gen_dirname(self):
        return datetime.date.today().strftime('%Y%m')

    def gen_filename(self):
        filename_prefix = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        return '%s%s' % (filename_prefix, str(random.randrange(1000, 10000)))

    def save(self):
        if current_app.config.get('COS_AK') and \
                current_app.config.get('COS_SK'):
            return self.qiniu_save_file()
        return self.local_save_file()

    def cos_save_file(self):
        pass

    def local_save_file(self):
        '''保存文件到static目录'''
        error = None
        UPLOAD_FOLDER = os.path.join(current_app.static_folder, 'uploadfiles')
        filepath = os.path.join(UPLOAD_FOLDER, self.filename)

        # 检查路径是否存在，不存在则创建
        dirname = os.path.dirname(filepath)
        if not os.path.exists(dirname):
            try:
                os.makedirs(dirname)
            except:
                error = 'ERROR_CREATE_DIR'
        elif not os.access(dirname, os.W_OK):
            error = 'ERROR_DIR_NOT_WRITEABLE'

        if not error:
            with open(filepath, 'wb') as fp:
                fp.write(self.data)
            return url_for('static', filename='%s/%s' % ('uploadfiles', self.filename))
        return ''

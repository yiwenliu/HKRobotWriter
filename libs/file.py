#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by yiwen on 2017/4/15

import codecs
import os


class FileHandle(object):
    def __init__(self, filepath, mode='r', encoding='utf-8'):
        assert os.path.exists(filepath), "argument to FileHandle must be a existed file"
        self.fp = codecs.open(filepath, mode, encoding)

    def __del__(self):
        self.fp.flush()
        self.fp.close()

    def read_all(self):
        """Read all the content of the file in UNICODE
        :return: u'...'
        """
        return self.fp.read()

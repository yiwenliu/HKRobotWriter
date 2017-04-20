#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by yiwen on 2017/4/10

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
log_path = 'log.log'
fh = logging.FileHandler(log_path)
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

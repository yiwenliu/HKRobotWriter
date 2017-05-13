#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by yiwen on 2017/4/23

import os, sys
sys.path.append(os.path.abspath(os.path.join(sys.path[0],os.pardir)))
from fetcher import *
from jobs import *
from processor import *
from template_handler import *
from libs.file import *
import json
pardir_abspath = os.path.abspath(os.path.join(sys.path[0], os.pardir))

from libs.smtp_client import *

if __name__ == '__main__':
    msg = 'test body'
    subject = 'test subject'
    print send_email(msg, subject)
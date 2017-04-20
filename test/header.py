#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by yiwen on 2017/4/16

import os, sys
sys.path.append(os.path.abspath(os.path.join(sys.path[0],os.pardir)))

from template_handler import *
from fetcher import *
from processor import *
from libs import log
import re
import time

trade_day_status = ("早盘竞价中", "交易中", "中午休市", "已收盘")
price_pattern = re.compile(r'\d+(\.\d+)?')
#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by yiwen on 2017/4/20

import os
import sys

sys.path.append(os.path.abspath(os.path.join(sys.path[0], os.pardir)))
from jobs import *
from template_handler import *
from libs.file import *

pardir_abspath = os.path.abspath(os.path.join(sys.path[0], os.pardir))
if __name__ == "__main__":
    '''
    gold_param = GoldHtmlParser(fetch_gold())
    print gold_param.get_date()
    '''
    print write_opening_gold_en()
    print write_closing_gold_en()
    # print USDHKDHtmlParser(fetch_usd_hkd()).get_value()

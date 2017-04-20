#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by yiwen on 2017/4/19

import os, sys
sys.path.append(os.path.abspath(os.path.join(sys.path[0],os.pardir)))
from fetcher import *
from jobs import *
from processor import *
from template_handler import *
from libs.file import *
import json

pardir_abspath = os.path.abspath(os.path.join(sys.path[0], os.pardir))

if __name__ == "__main__":
    ###initialization(start)
    sp = json.loads(FileHandle('closing_stocks_param').read_all())  # type(sp) is dict
    p = {}
    for key in sp:
        p[key] = StockParser(sp[key])
    individual_stock = p['00700']
    ###initialization(end)
    #print ClosingIndividualStockCnMaker.do(individual_stock)
    #print ClosingStockPartCnMaker.do(p)
    #print write_closing_index_stock_cn()
    print write_closing_future_index_cn()
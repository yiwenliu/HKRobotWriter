#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by yiwen on 2017/4/13
import os, sys
sys.path.append(os.path.abspath(os.path.join(sys.path[0],os.pardir)))
from fetcher import *
from jobs import *
from processor import *
from template_handler import *
from libs.file import *
import json
r_am_closing_index = '{"code":0,"msg":"\u83b7\u53d6\u6210\u529f","data":{"symbol":"HSI","status":1,"status_descip":"\u4e2d\u5348\u4f11\u5e02","name":"\u6052\u751f\u6307\u6570","price":"24054.39","zhangdiee":"-207.79","zhangdiefu":"-0.86%","chengjiaoe":"426.68\u4ebf","jinkaijia":"24280.87","zuoshoujia":"24262.18","zuigaojia":"24318.15","zuidijia":"24029.69","zhouzuigaojia":"24656.65","zhouzuidijia":"19594.61","riqi":"04-11","shijian":"12:05:00","zhenfu":"1.19%","market":"hk"}}'
r_closing_index = '{"code":0,"msg":"\u83b7\u53d6\u6210\u529f","data":{"symbol":"HSCEI","status":2,"status_descip":"\u5df2\u6536\u76d8","name":"\u6052\u751f\u4e2d\u56fd\u4f01\u4e1a\u6307\u6570","price":"10273.80","zhangdiee":"-2.61","zhangdiefu":"-0.03%","chengjiaoe":"163.45\u4ebf","jinkaijia":"10269.84","zuoshoujia":"10276.41","zuigaojia":"10282.20","zuidijia":"10147.54","zhouzuigaojia":"10698.28","zhouzuidijia":"8175.96","riqi":"04-07","shijian":"16:09:32","zhenfu":"1.31%","market":"hk"}}'

if __name__ == "__main__":
    os.chdir(os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), os.pardir)))
    #print 'Now working dir is {}'.format(os.getcwd())
    #write_opening_index_en()
    #write_opening_gold_en()

    #write_morning_closing_index_en(demo=r_am_closing_index)

    #write_closing_fx_en()
    #write_closing_index_en()
    #write_closing_index_stock_cn()
    write_closing_future_index_cn()

    #write_closing_gold_en()





#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by yiwen on 2017/4/10

import time
import schedule
import os
import sys


if __name__ == "__main__":
    os.chdir(os.path.abspath(os.path.dirname(sys.argv[0]))) #very important, because the template handler use the relative path
    print("CURRENT DIRECTORY is {}".format(os.getcwd()))
    from jobs import *
    '''
    schedule.every().day.at("9:24").do(write_opening_index_en)
    schedule.every().day.at("9:25").do(write_opening_gold_en)
    schedule.every().day.at("12:00").do(write_morning_closing_index_en)
    schedule.every().day.at("16:30").do(write_closing_index_en)
    schedule.every().day.at("16:30").do(write_closing_index_stock_cn)
    schedule.every().day.at("16:30").do(write_closing_future_index_cn)
    schedule.every().day.at("16:30").do(write_closing_fx_en)
    '''
    schedule.every().day.at("9:25").do(write_opening_09_30)
    schedule.every().day.at("12:00").do(write_morning_closing_index_en)
    schedule.every().day.at("16:30").do(write_closing_16_30)
    schedule.every().day.at("17:00").do(write_closing_gold_en)
    while True:
        schedule.run_pending()
        time.sleep(5)

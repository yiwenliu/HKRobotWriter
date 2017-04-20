#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by yiwen on 2017/4/10

import time
import schedule
from jobs import *

if __name__ == "__main__":
    schedule.every().day.at("9:24").do(write_opening_index_en)
    schedule.every().day.at("12:00").do(write_morning_closing_index_en)
    schedule.every().day.at("16:30").do(write_closing_index_en)
    schedule.every().day.at("16:30").do(write_closing_index_stock_cn)
    schedule.every().day.at("16:30").do(write_closing_future_index_cn)
    schedule.every().day.at("16:30").do(write_closing_fx_en)
    schedule.every().day.at("9:25").do(write_opening_gold_en)
    schedule.every().day.at("17:00").do(write_closing_gold_en)
    while True:
        schedule.run_pending()
        time.sleep(5)

#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by yiwen on 2017/4/15

import os
import sys

sys.path.append(os.path.abspath(os.path.join(sys.path[0],os.pardir)))
from template_handler import TemplateHandle

class write(object):
    """Put the data and template together
    Attributes:
        transaction_time: IN 'opening', 'closing', 'morning closing'
        asset_class: IN 'index', 'fx', 'gold'...
        lan: IN 'en', 'cn'
        rps: object of Class Parser
        work: article done by making up data and template
    """
    def __init__(self, transaction_time, asset_class, lan, response):
        self.transaction_time = transaction_time
        self.asset_class = asset_class
        self.lan = lan
        self.rps = response
        self.pardir_abspath = os.path.abspath(os.path.join(sys.path[0],os.pardir))
        self.work = ''

    def do(self):
        if self.transaction_time == 'opening':
            if self.asset_class == 'index':
                self.write_opening_index()
            if self.asset_class == 'gold':
                self.write_opening_gold()
        if self.transaction_time == 'morning closing':
            if self.asset_class == 'index':
                self.write_morning_closing_index()
        if self.transaction_time == 'closing':
            if self.asset_class == 'index':
                self.write_closing_index()
            if self.asset_class == ['index', 'stock']:
                self.write_closing_index_stock()
            if self.asset_class == ['futre', 'index']:
                self.write_closing_future_index()
            if self.asset_class == 'gold':
                self.write_closing_gold()
            if self.asset_class == 'fx':
                self.write_clsing_fx()

    def write_opening_index(self):
        '''
        template_file_name = "opening_index_" + self.lan
        template_path = os.path.join(self.pardir_abspath, 'templates', template_file_name)
        template_content = FileHandle(template_path).read_all()
        '''
        th = TemplateHandle("opening_index_" + self.lan)
        tc = th.get_template_contnt()


    def write_opening_gold(self):
        template_file_name = "opening_gold_" + self.lan
        template_path = os.path.join(self.pardir_abspath, 'templates', template_file_name)


    def write_morning_closing_index(self):
        template_file_name = "morning_closing_index_" + self.lan
        template_path = os.path.join(self.pardir_abspath, 'templates', template_file_name)

    def write_closing_index(self):
        template_file_name = "closing_index_" + self.lan
        template_path = os.path.join(self.pardir_abspath, 'templates', template_file_name)

    def write_closing_index_stock(self):
        pass

    def write_closing_future_index(self):
        template_file_name = "closing_future_index_" + self.lan
        template_path = os.path.join(self.pardir_abspath, 'templates', template_file_name)

    def write_closing_gold(self):
        template_file_name = "closing_gold_" + self.lan
        template_path = os.path.join(self.pardir_abspath, 'templates', template_file_name)

    def write_clsing_fx(self):
        template_file_name = "closing_fx_" + self.lan
        template_path = os.path.join(self.pardir_abspath, 'templates', template_file_name)
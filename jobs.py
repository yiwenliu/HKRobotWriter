#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by yiwen on 2017/4/15
from template_handler import *
from fetcher import *
from processor import *
from libs import log
import re
import time


def write_opening_index_en(*args, **kwargs):
    work = ""
    point_pattern = re.compile(r'\d+(\.\d+)?')  # "24280.87"
    while True:
        if len(kwargs) > 0:  # In unit test mode
            hsi_parser = IndexParser(kwargs['demo'])
        else:
            hsi_parser = IndexParser(fetch_index()['HSI'])
        if hsi_parser.get_status() not in hsi_parser.trade_day_status:
            log.logger.info("Write Index Opening -- Non-trading day")
            break
        else:
            if point_pattern.match(hsi_parser.get_opening_point()):
                template_handler = OpeningIndexEnMaker("opening_index_en")
                work = template_handler.do(hsi_parser)
                break
            else:
                time.sleep(10)
    return work


def write_morning_closing_index_en(*args, **kwargs):
    """
    :param args: for unit test
    :param kwargs: for unit test
    :return: 
    """
    work = ""
    while True:
        if len(kwargs) > 0:  # In unit test mode
            # print kwargs['response']
            hsi_parser = IndexParser(kwargs['demo'])
        else:
            hsi_response = fetch_index()['HSI']
            # print hsi_response
            hsi_parser = IndexParser(hsi_response)
        if hsi_parser.get_status() not in hsi_parser.trade_day_status:
            log.logger.info("Write Index Morning Closing -- Non-trading day")
            break
        else:
            if hsi_parser.get_status() == hsi_parser.trade_day_status[2]:
                template_handler = MorningClosingIndexEnMaker("morning_closing_index_en")
                work = template_handler.do(hsi_parser)
                log.logger.info("Write Index Morning Closing -- OK")
                break
            else:
                if len(kwargs) > 0:  # In unit test mode
                    break
                else:
                    time.sleep(10)
    return work


def write_closing_index_en(*args, **kwargs):
    work = ""
    while True:
        if len(kwargs) > 0:  # In unit test mode
            hsi_parser = IndexParser(kwargs['demo'])
        else:
            hsi_parser = IndexParser(fetch_index()['HSI'])
        if hsi_parser.get_status() not in hsi_parser.trade_day_status:
            log.logger.info("Write Index Closing -- Non-trading day:%s" % (hsi_parser.get_status()))
            break
        else:
            if hsi_parser.get_status() == hsi_parser.trade_day_status[3]:
                hsi_parser.usd_hkd_fx = "%.3f" % (float(hsi_parser.get_turnover()[1]) / float(
                    USDHKDHtmlParser(fetch_usd_hkd()).get_value()))  # get the instant fx from yahoo
                template_handler = ClosingIndexEnMaker("closing_index_en")
                work = template_handler.do(hsi_parser)
                log.logger.info("Write Index Closing -- OK")
                break
            else:
                if len(kwargs) > 0:  # In unit test mode
                    break
                else:
                    time.sleep(10)
    return work


def write_closing_index_stock_cn(*args, **kwargs):
    work = ""
    securities = {'index': {}, 'stock': {}}
    while True:
        if len(kwargs) > 0:  # If in unit test mode
            pass
        else:
            index_response = fetch_index()  # {'HSI':{...}, 'HSCEI':{...}}
            stock_response = fetch_stock()  # {'00700':{...}, '00388':{...}...}
            # print stock_response
            # break
            for key in index_response:
                securities['index'][key] = IndexParser(index_response[key])
            for key in stock_response:
                securities['stock'][key] = StockParser(stock_response[key])
        if securities['index']['HSI'].get_status() not in JsonParser.trade_day_status:
            log.logger.info(
                "Write index and stock Closing -- Non-trading day:%s" % (securities['index']['HSI'].get_status()))
            break
        else:
            if securities['index']['HSI'].get_status() == JsonParser.trade_day_status[3]:
                work = ClosingSecurityCnMaker.do(securities)
                log.logger.info("Write Security Closing -- OK")
                break
            else:  # The security market is not close yet
                if len(kwargs) > 0:  # In unit test mode
                    break
                else:
                    time.sleep(10)
    return work


def write_closing_future_index_cn(*args, **kwargs):
    work = ""
    securities = {'index': {}}
    while True:
        if len(kwargs) > 0:  # If in unit test mode
            pass
        else:
            index_response = fetch_index()  # {'HSI':{...}, 'HSCEI':{...}}
            future_response = fetch_future()  # {'00700':{...}, '00388':{...}...}
            for key in index_response:
                securities['index'][key] = IndexParser(index_response[key])
            securities['future'] = FutureParser(future_response)
        if securities['index']['HSI'].get_status() not in JsonParser.trade_day_status:
            log.logger.info(
                "Write future and index Closing -- Non-trading day:%s" % (securities['index']['HSI'].get_status()))
            break
        else:
            if securities['index']['HSI'].get_status() == JsonParser.trade_day_status[3]:
                work = ClosingFutureIndexCnMaker.do(securities)
                log.logger.info("Write future and index Closing -- OK")
                break
            else:  # The security market is not close yet
                if len(kwargs) > 0:  # In unit test mode
                    break
                else:
                    time.sleep(10)
    return work


def write_opening_gold_en():
    work = ''
    gold_param = GoldHtmlParser(fetch_gold())
    if time.strftime("%Y.%m.%d") == gold_param.get_latest_date():
        usd_hkd_fx = USDHKDHtmlParser(fetch_usd_hkd()).get_value()
        work = OpeningGoldEnMaker.do(gold_param, usd_hkd_fx)
        log.logger.info("Write gold opening -- OK.")
    else:
        log.logger.info(
            "Write future and index Closing -- Non-trading day.")
    return work


def write_closing_gold_en():
    work = ''
    gold_param = GoldHtmlParser(fetch_gold())
    if time.strftime("%Y.%m.%d") == gold_param.get_latest_date():
        work = ClosingGoldEnMaker.do(gold_param)
        log.logger.info("Write gold closing -- OK.")
    else:
        log.logger.info(
            "Write future and index Closing -- Non-trading day.")
    return work


def write_closing_fx_en():
    return ClosingFXEnMaker.do(FXHtmlParser(fetch_fx()))

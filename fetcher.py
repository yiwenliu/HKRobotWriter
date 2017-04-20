#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import time
from libs.http import http_client


def fetch_index():
    """
    :return: {'HSI':{...}, 'HSCEI':{...}}
    """
    url_template = 'http://api.ggt.sina.com.cn/ggtapi/getSymbolQuotation.php?deviceModel=iPhone&versionId=2.2.0' \
                   '&deviceNum=202B8E34-5BC2-4B9B-8F9C-3D4D384D932F&ggtChannelId=10101&symbol=hk{{' \
                   'index_symbol}}&type=1 '
    index_list = ['HSI', 'HSCEI']
    index_params_dict = {}
    headers = {'User-Agent': "GGT-iOS/2.2.0 (iPhone; iOS 9.3.5; Scale/2.00)",
               'Connection': 'keep-alive',
               'Accept-Encoding': 'gzip, deflate, sdch',
               'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
               'Accept': '*/*'}
    '''
    cookies = {'sinaH5EtagStatus':'y', 'Apache':'218.255.224.114_1491579529.466685', 'SINAGLOBAL':'218.255.224.114_1491579529.466681',
               'ULV':'1491579529425:1:1:1::', 'UOR':',api.ggt.sina.com.cn,', 'U_TRS1':'00000072.a25a3955.58e7b289.f240b42d',
               'U_TRS2':'00000072.a2653955.58e7b289.9d196cc1'}
    '''
    for item in index_list:
        index_params_dict[item] = http_client(symbol=item, url=url_template.replace("{{index_symbol}}", item),
                                              headers=headers)
    return index_params_dict


def fetch_stock():
    """
    :return: {'00700':{...}, '00388':{...}...}
    """
    url_template = 'http://api.ggt.sina.com.cn/ggtapi/getSymbolQuotation.php?deviceModel=iPhone&versionId=2.2.0' \
                   '&deviceNum=202B8E34-5BC2-4B9B-8F9C-3D4D384D932F&ggtChannelId=10101&symbol=hk{{code}}&type=2 '
    symbol_list = ['00700', '00388', '00941', '00005', '01113', '00016', '00012', '03988', '00939',
                   '01398', '02318', '02628', '00386', '00857', '00883']
    stock_params_dict = {}
    headers = {'User-Agent': "GGT-iOS/2.2.0 (iPhone; iOS 9.3.5; Scale/2.00)",
               'Connection': 'keep-alive',
               'Accept-Encoding': 'gzip, deflate, sdch',
               'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
               'Accept': '*/*'}
    for item in symbol_list:
        stock_params_dict[item] = http_client(symbol=item, url=url_template.replace("{{code}}", item), headers=headers)
    return stock_params_dict


def fetch_future():
    """
    Variables:
      url_list: [http://stock360.hkej.com/data/getWorldIndices?t=1491986953256]
    :return: 
    """
    url_template = "http://stock360.hkej.com/data/getWorldIndices?t={{timestamp}}"
    ts_str = ''.join(('%.3f' % time.time()).split('.'))
    return http_client(symbol='FUTURE', url=url_template.replace("{{timestamp}}", ts_str))


def fetch_gold():
    url_template = "http://www.cgse.com.hk/cn/price_02.php?searchdate={{date}}&sproduct_id=1&x=37&y=7&issubmit=Y"
    today_date = time.strftime("%Y-%m-%d", time.localtime())
    return http_client(symbol='GOLD', url=url_template.replace('{{date}}', today_date))


def fetch_fx():
    url_template = "https://bank.hangseng.com/1/2/rates/foreign-currency-tt-exchange-rates"
    return http_client(symbol='FX', url=url_template)


def fetch_usd_hkd():
    url_template = "https://hk.finance.yahoo.com/quote/USDHKD=x?ltr=1"
    return http_client(symbol='USDHKD', url=url_template)

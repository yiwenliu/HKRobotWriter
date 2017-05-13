#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by yiwen on 2017/4/10

import json
from bs4 import BeautifulSoup
import bs4
import time


class Parser(object):
    def __init__(self, response):
        #assert isinstance(response, basestring), "response to parse must be a string"
        #print 'the type of response is {}'.format(typeof(response))
        self.content = response

    def get_date(self, lang='en'):
        if lang == 'en':
            return "%s %d" % (time.strftime("%B", time.localtime()), int(time.strftime("%d", time.localtime())))

    def get_week_day(self):
        return time.strftime("%A", time.localtime())

    def get_day(self):
        return time.strftime("%d", time.localtime())

    def get_month(self):
        return time.strftime("%m", time.localtime())


class JsonParser(Parser):
    """
    Attributes:
        content_dict: unicode
    """
    trade_day_status = ("早盘竞价中", "交易中", "中午休市", "已收盘")

    def __init__(self, response):
        Parser.__init__(self, response)
        self.content_dict = json.loads(self.content)


class StockParser(JsonParser):
    def __init__(self, response):
        JsonParser.__init__(self, response)
        self.param_dict = self.content_dict[u'data']

    def get_closing_price(self):
        '''
        :return: '48.850' -> '48.85'
        '''
        #return self.param_dict[u'price'].encode('utf-8').strip()
        return "{:.2f}".format(float(self.param_dict[u'price']))

    def get_closing_change(self):
        """
        Variables:
          ratio: u"+0.71%"
        :return: ('+', "0.71")
        """
        ratio = self.param_dict[u'zhangdiefu']
        #return ratio[0].encode('utf-8'), ratio[1:-1].encode('utf-8')
        return ratio[0], ratio[1:-1]

    def get_name(self):
        return self.param_dict[u'name']


class IndexParser(JsonParser):
    """
    Attributes:
        param_dict:{
        "symbol": "HSI",
        "status": 1,
        "status_descip": "交易中",
        "name": "恒生指数",
        "price": "24045.85",
        "zhangdiee": "-42.61",
        "zhangdiefu": "-0.18%",
        "chengjiaoe": "263.16亿",
        "jinkaijia": "24068.91",
        "zuoshoujia": "24088.46",
        "zuigaojia": "24073.11",
        "zuidijia": "23994.13",
        "zhouzuigaojia": "24656.65",
        "zhouzuidijia": "19594.61",
        "riqi": "04-12",
        "shijian": "10:56:50",
        "zhenfu": "0.33%",
        "market": "hk"
        }
    """

    def __init__(self, response):
        JsonParser.__init__(self, response)
        self.param_dict = self.content_dict[u'data']

    def get_name(self, coding='utf-8'):
        return self.param_dict[u'name'] if coding == 'unicode' else self.param_dict[u'name'].encode('utf-8')

    def get_last_update_date(self):
        return self.param_dict[u'']

    def get_opening_point_raw(self):
        """Get the raw opening point in unicode from the json returned
        Returns:
            u'24280.87'
        """
        return self.param_dict[u'jinkaijia']

    def get_opening_point(self):
        """Get the opening point formatted
        Returns:
            '24280.87'
        """
        return self.get_opening_point_raw().encode('utf-8').strip()

    def get_max_point(self):
        return self.param_dict[u'zuigaojia'].encode('utf-8').strip()

    def get_min_point(self):
        return self.param_dict[u'zuidijia'].encode('utf-8').strip()

    def get_closing_point(self, coding='utf-8'):
        return self.param_dict[u'price'] if coding == 'unicode' else self.param_dict[u'price'].encode('utf-8').strip()

    def get_turnover(self):
        """
        Variables:
          self.param_dict[u'chengjiaoe']:u"163.45\u4ebf(亿)"
          num:u"163.45", but the quantity unit is billion(十亿). 
              Another question, Is the monetary unit is HK dollar?
        :return: (u"163.45", "16.345")
        """
        num = self.param_dict[u'chengjiaoe'][:-1]
        num1 = "%.3f" % (float(num.encode('utf-8')) / 10)
        return num, num1

    def get_price(self):
        return self.param_dict[u'price']

    def get_status(self):
        return self.param_dict[u'status_descip'].encode('utf-8').strip()

    def get_index_symbol(self):
        return self.param_dict[u'symbol']

    def get_opening_change(self):
        """the change and ratio when opening
        :return: ('-', '90.39', '0.37')
        """
        if self.get_status() != self.trade_day_status[0]:
            opening_price = float(self.param_dict[u'jinkaijia'].encode('utf-8'))
            yesterday_closing_price = float(self.param_dict[u'zuoshoujia'].encode('utf-8'))
            change = round((opening_price - yesterday_closing_price), 2)
            ratio = round((abs(change) / yesterday_closing_price) * 100, 2)
            up_or_down = '+' if change > 0 else '-'
            return up_or_down, "%.2f" % abs(change), "%.2f" % ratio
        else:
            return self.get_morning_session_change()

    def get_morning_session_change(self):
        """the change and ratio when morning session closed
        :return: ('+', '90.39', '0.37')
        """
        change = self.param_dict[u'zhangdiee'].strip().encode('utf-8')
        ratio = self.param_dict[u'zhangdiefu'].strip().encode('utf-8')
        up_or_down = change[0]
        return up_or_down, change[1:], ratio[1:-1]

    def get_closing_change(self):
        """the change and ratio when market closed
        :return: ('+', '90.39', '0.37')
        """
        return self.get_morning_session_change()


class FutureParser(JsonParser):
    """Get the parameters from the json response
    在一个类中同时解析恒指和国指期货的原因是这两者的参数在一个json响应中，而不像index。
    Attributes:
        param_dict:{
        "HSIF1":{
                Symbol: "HSIF1",
                ChiName: "恒指期貨日市(即月)",
                ...
                },
        "HHIF1":{
                Symbol: "HHIF1",
                ChiName: "國指期貨日市(即月)",
                }
    """

    def __init__(self, response):
        JsonParser.__init__(self, response)
        self.future_symbol_list = [u'HSIF1', u'HHIF1']
        future_list = [item for item in self.content_dict[u'wdata'] if item[u'Symbol'] in self.future_symbol_list]
        self.param_dict = {}
        for item in future_list:
            self.param_dict[item[u'Symbol']] = item

    def get_last_update_date(self, symbol):
        return self.param_dict[symbol][u'lastupdate']

    def get_opening_price(self, symbol):
        return self.param_dict[symbol][u'Open']

    def get_max_price(self, symbol):
        return self.param_dict[symbol][u'High']

    def get_min_price(self, symbol):
        return self.param_dict[symbol][u'Low']

    def get_closing_point(self, symbol):
        return self.param_dict[symbol][u'Last']

    def get_volume(self, symbol):
        return self.param_dict[symbol][u'Volume']

    def get_closing_change(self, symbol):
        """get the change and ratio when market closed.
        :return: (u'-', u'43')
        """
        change = float(self.param_dict[symbol][u'Last'].encode("utf-8")) - float(
            self.param_dict[symbol][u'PrevClose'].encode("utf-8"))
        up_or_down = u'+' if change > 0 else u'-'
        return up_or_down, str("%d" % (abs(change))).decode('utf-8')


class HtmlParser(Parser):
    def __init__(self, response):
        Parser.__init__(self, response)
        self.soup = BeautifulSoup(self.content, "lxml")


class USDHKDHtmlParser(HtmlParser):
    """Needed when writing index closing article.
    """
    def __init__(self, response):
        HtmlParser.__init__(self, response)
        #self.usdhkd = self.soup.find("div", id="quote-market-notice").parent.span.string.encode('utf-8').strip()

    def get_value(self):
        return self.soup.find("div", id="quote-market-notice").parent.span.string.encode('utf-8').strip()
        #return self.usdhkd


class GoldHtmlParser(HtmlParser):
    """Get the parameters from the response of http://www.cgse.com.hk/
    Attributes:
        latest_params_list: the latest data:[u'2017.04.11', u'11640', u'11665', u'11635', None, u'-348.75']
    """

    def __init__(self, response):
        HtmlParser.__init__(self, response)
        tr_tag = [item for item in self.soup.find("td", text=u"日期").parent.next_siblings if
                  type(item) is bs4.element.Tag]
        latest_tr_tag = tr_tag[0]
        last_tr_tag = tr_tag[1]
        self.latest_params_list = [item.string for item in latest_tr_tag.find_all("div")]
        self.last_params_list = [item.string for item in last_tr_tag.find_all("div")]

    def get_latest_date(self):
        return self.latest_params_list[0]

    def get_opening_price(self):
        return self.latest_params_list[1].strip()

    def get_max_price(self):
        return self.latest_params_list[2]

    def get_min_price(self):
        return self.latest_params_list[3]

    def get_closing_price(self):
        return self.latest_params_list[4]

    def get_opening_change(self):
        """
        :return: (u'+', '20')
        """
        change = int(self.latest_params_list[1].encode("utf-8")) - int(self.last_params_list[4].encode("utf-8"))
        up_or_down = u'+' if change > 0 else u'-'
        return up_or_down, '%d' % (abs(change))

    def get_closing_change(self):
        """
        :return: (u'+', '20')
        """
        change = int(self.latest_params_list[4].encode("utf-8")) - int(self.last_params_list[4].encode("utf-8"))
        up_or_down = u'+' if change > 0 else u'-'
        return up_or_down, '%d' % (abs(change))


class FXHtmlParser(HtmlParser):
    """
    Attributes:
        currency_list: the currency name on the website
        cur_dict = {u'AUD': (u'5.7960', u'5.8750'),
                    u'CAD': (u'5.7970', u'5.8750'),
                    u'CHF': (u'7.6670', u'7.7630'),
                    u'EUR': (u'8.1920', u'8.3020'),
                    u'GBP': (u'9.5990', u'9.7190'),
                    u'JPY': (u'69.7100', u'70.8100'),
                    u'USD': (u'7.7570', u'7.7870')}
    """

    def __init__(self, response):
        HtmlParser.__init__(self, response)
        self.currency_list = [u'US Dollar', u'Australian Dollar', u'Canadian Dollar', u'Swiss Franc', u'Euro',
                              u'Pound Sterling', u'Japanese Yen\xa0(per 1,000)']
        cur_td_list = [item for item in self.soup.find_all("td") if item.text.strip() in self.currency_list]
        self.cur_dict = {}
        for item in cur_td_list:
            item_list = [item1 for item1 in item.next_siblings if type(item1) is bs4.element.Tag]
            self.cur_dict[item_list[0].text] = ("{:.2f}".format(float(item_list[1].text)*100), "{:.2f}".format(float(item_list[2].text)*100))

    def get_rate(self):
        return self.cur_dict

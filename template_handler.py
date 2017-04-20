#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by yiwen on 2017/4/15
from libs.file import FileHandle
import os, sys
import time

# sys.path.append(os.path.abspath(os.path.join(sys.path[0],os.pardir)))
pardir_abspath = os.path.abspath(os.path.join(sys.path[0], os.pardir))


class Maker(object):
    pardir_abspath = os.path.abspath(os.path.join(sys.path[0], os.pardir))

    def __init__(self, template_name):
        template_path = os.path.join(Maker.pardir_abspath, 'templates', template_name)
        self.template_handle = FileHandle(template_path)
        self.template_content = self.template_handle.read_all().encode('utf-8')

    def get_template_contnt(self):
        return self.template_handle.read_all().encode('utf-8')

    def do(self, r):
        """
        :param r: object of class Parser out of the http response
        :return: 
        """
        pass


class ClosingFutureIndexMaker(Maker):
    pass


class OpeningIndexEnMaker(Maker):
    def do(self, r):
        # template_content = self.get_template_contnt()
        change_params = r.get_opening_change()
        verb = "gained" if change_params[0] == '+' else 'lost'
        return self.template_content.format(date=r.get_date(), up_or_down=verb, change_point=change_params[1],
                                            change_rate=change_params[2],
                                            point="{:,}".format(float(r.get_opening_point())),
                                            weekday=r.get_week_day())


class MorningClosingIndexEnMaker(Maker):
    def do(self, r):
        # template_content = self.get_template_contnt()
        change_params = r.get_morning_session_change()
        verb = "gained" if change_params[0] == '+' else 'lost'
        # print r.get_price()
        return self.template_content.format(date=r.get_date(), up_or_down=verb, change_point=change_params[1],
                                            change_rate=change_params[2], point="{:,}".format(float(r.get_price())),
                                            weekday=r.get_week_day())


class ClosingIndexEnMaker(Maker):
    def do(self, r):
        change_params = r.get_closing_change()
        # print change_params
        prep = "up" if change_params[0] == '+' else 'down'
        return self.template_content.format(date=r.get_date(), up_or_down=prep, change_point=change_params[1],
                                            change_rate=change_params[2],
                                            point="{:,}".format(float(r.get_closing_point())),
                                            weekday=r.get_week_day(),
                                            high_point="{:,}".format(float(r.get_max_point())),
                                            low_point="{:,}".format(float(r.get_min_point())),
                                            turnover_hkd=r.get_turnover()[1],
                                            turnover_usd=r.usd_hkd_fx)


class ClosingIndexHSICnMaker(object):
    template_content = FileHandle(os.path.join(pardir_abspath, 'templates', 'closing_index_hsi_cn')).read_all()
    up_verb = u'\u6da8'  # 涨
    down_verb = u'\u8dcc'  # 跌

    @classmethod
    def do(cls, hsi):
        return cls.template_content.format(index_name=hsi.get_name(coding='unicode'),
                                           weekday=hsi.get_day().decode('utf-8'),
                                           up_or_down=cls.up_verb if hsi.get_closing_change()[
                                                                         0] == '+' else cls.down_verb,
                                           change_point=hsi.get_closing_change()[1].decode('utf-8'),
                                           change_rate=hsi.get_closing_change()[2].decode('utf-8'),
                                           closing_point=hsi.get_closing_point().decode('utf-8'),
                                           turnover=hsi.get_turnover()[0])


class ClosingIndexHSCEICnMaker(object):
    template_content = FileHandle(os.path.join(pardir_abspath, 'templates', 'closing_index_hscei_cn')).read_all()
    up_verb = u'\u6da8'  # 涨
    down_verb = u'\u8dcc'  # 跌

    @classmethod
    def do(cls, hscei):
        return cls.template_content.format(index_name=hscei.get_name(coding='unicode'),
                                           up_or_down=cls.up_verb if hscei.get_closing_change()[
                                                                         0] == '+' else cls.down_verb,
                                           change_point=hscei.get_closing_change()[1].decode('utf-8'),
                                           closing_point=hscei.get_closing_point().decode('utf-8'))


class ClosingIndexPartCnMaker(object):
    """
    template = "{index_name}{weekday}日{up_or_down}{change_point}点，{up_or_down}幅{change_rate}%，收报{closing_point}点。全日{" \
               "board_name}成交{turnover}亿港元。 "
    index_tuple = ('HSI', 'HSCEI')  # control the sequence of output
    """

    @classmethod
    def do(cls, index):
        work = u""
        work += ClosingIndexHSICnMaker.do(index['HSI'])
        work += u'\r\n'
        work += ClosingIndexHSCEICnMaker.do(index['HSCEI'])
        work += u'\r\n'
        return work


class ClosingIndividualStockCnMaker(object):
    template_content = FileHandle(os.path.join(pardir_abspath, 'templates', 'closing_individual_stock_cn')).read_all()
    up_verb = u'\u6da8'  # 涨
    down_verb = u'\u8dcc'  # 跌

    @classmethod
    def do(cls, individual_stock):
        """
        :param individual_stock: object_of_StockParser
        :return: 
        """
        # print individual_stock.get_name(), individual_stock.get_closing_change()[0], individual_stock.get_closing_change()[1], individual_stock.get_closing_price()
        return cls.template_content.format(stock_name=individual_stock.get_name(),
                                           up_or_down=cls.down_verb if individual_stock.get_closing_change()[
                                                                           0] == u'-' else cls.up_verb,
                                           change_rate=individual_stock.get_closing_change()[1],
                                           closing_price=individual_stock.get_closing_price())


class ClosingBoardCnMaker(object):
    @classmethod
    def do(cls, board_name, stock_tuple, stock_params):
        """
        :param board_name: e.g."蓝筹股"
        :param stock_tuple: ("00700", "00038",...)
        :param stock_params: {'00700': object_of_StockParser, '00388':object_of_StockParser...}
        :return: e.g.蓝筹股方面，腾讯跌0.350%，收报228港币；...
        """
        work = (board_name + '方面，').decode('utf-8')
        for stock_code in stock_tuple:
            work += ClosingIndividualStockCnMaker.do(stock_params[stock_code])
        work = work[:-1] + '。'.decode('utf-8')
        return work


class ClosingStockPartCnMaker(object):
    header = "{board_name}方面"
    boards = ("蓝筹股", "香港本地股", "中资金融股", "石油石化股")
    board_stock = {"蓝筹股": ("00700", "00388", "00941", "00005"),
                   "香港本地股": ("01113", "00016", "00012"),
                   "中资金融股": ("03988", "00939", "01398", "02318", "02628"),
                   "石油石化股": ("00386", "00857", "00883")}

    @classmethod
    def do(cls, stock_params):
        """
        :param stock_params: {'00700': object_of_StockParser, '00388':object_of_StockParser...}
        :return: 
        """
        work = u''
        for board_name in cls.boards:
            work += ClosingBoardCnMaker.do(board_name, cls.board_stock[board_name], stock_params)
            work += u'\r\n'
        return work


class ClosingSecurityCnMaker(object):
    header = '新华社香港{month}月{day}日电 '.decode('utf-8')
    end = '（完）'.decode('utf-8')

    @classmethod
    def do(cls, securities):
        m = time.strftime("%m", time.localtime()).decode('utf-8')
        d = time.strftime("%d", time.localtime()).decode('utf-8')
        return cls.header.format(month=m, day=d) + ClosingIndexPartCnMaker.do(
            securities['index']) + ClosingStockPartCnMaker.do(securities['stock']) + cls.end


class ClosingFutureIndexCnMaker(object):
    template_content = FileHandle(os.path.join(pardir_abspath, 'templates', 'closing_future_index_cn')).read_all()

    @classmethod
    def do(cls, fi):
        hsi = fi['index']['HSI']
        hscei = fi['index']['HSCEI']
        future = fi['future']
        m = time.strftime("%m", time.localtime()).decode('utf-8')
        d = time.strftime("%d", time.localtime()).decode('utf-8')
        return cls.template_content.format(month=m, day=d, turnover=hsi.get_turnover()[0],
                                           hsi_opening_point=hsi.get_opening_point_raw(),
                                           hsi_closing_point=hsi.get_closing_point(coding='unicode'),
                                           hsi_change_point=(
                                           hsi.get_closing_change()[0] + hsi.get_closing_change()[1]).decode('utf-8'),
                                           hscei_opening_point=hscei.get_opening_point_raw(),
                                           hscei_closing_point=hscei.get_closing_point(coding='unicode'),
                                           hscei_change_point=(
                                           hscei.get_closing_change()[0] + hsi.get_closing_change()[1]).decode('utf-8'),
                                           hsif1_closing_point=future.get_closing_point(u'HSIF1'),
                                           hsif1_change_point=future.get_closing_change(u'HSIF1')[0] +
                                                              future.get_closing_change(u'HSIF1')[1],
                                           hsif1_volume=future.get_volume(u'HSIF1'),
                                           hhif1_closing_point=future.get_closing_point(u'HHIF1'),
                                           hhif1_change_point=future.get_closing_change(u'HHIF1')[0] +
                                                              future.get_closing_change(u'HHIF1')[1],
                                           hhif1_volume=future.get_volume(u'HHIF1'),
                                           )


class OpeningGoldEnMaker(object):
    template_content = FileHandle(os.path.join(pardir_abspath, 'templates', 'opening_gold_en')).read_all()

    @classmethod
    def do(cls, gold, usd_hk_fx):
        return cls.template_content.format(date=gold.get_date(),
                                           up_or_down='went up' if gold.get_opening_change()[0] == u'+' else 'went down',
                                           opening_change_price=gold.get_opening_change()[1],
                                           opening_price="{:,}".format(int(gold.get_opening_price())),
                                           week=gold.get_week_day(),
                                           usd_fx_hkd=usd_hk_fx)

class ClosingGoldEnMaker(object):
    template_content = FileHandle(os.path.join(pardir_abspath, 'templates', 'closing_gold_en')).read_all()

    @classmethod
    def do(cls, gold):
        return cls.template_content.format(date=gold.get_date(),
                                           closing_price="{:,}".format(int(gold.get_closing_price())),
                                           week=gold.get_week_day(),
                                           up_or_down='up' if gold.get_closing_change()[0] == u'+' else 'down',
                                           change_price=gold.get_closing_change()[1],
                                           )

class ClosingFXEnMaker(object):
    template_content = FileHandle(os.path.join(pardir_abspath, 'templates', 'closing_fx_en')).read_all()

    @classmethod
    def do(cls, fx):
        return cls.template_content.format(date=fx.get_date(),week=fx.get_week_day(),
                                           usd_b=fx.get_rate()['USD'][0], usd_s=fx.get_rate()['USD'][1],
                                           aud_b=fx.get_rate()['AUD'][0], aud_s=fx.get_rate()['AUD'][1],
                                           cad_b=fx.get_rate()['CAD'][0], cad_s=fx.get_rate()['CAD'][1],
                                           chf_b=fx.get_rate()['CHF'][0], chf_s=fx.get_rate()['CHF'][1],
                                           eur_b=fx.get_rate()['EUR'][0], eur_s=fx.get_rate()['EUR'][1],
                                           gbp_b=fx.get_rate()['GBP'][0], gbp_s=fx.get_rate()['GBP'][1],
                                           jpy_b="{:.2f}".format(float(fx.get_rate()['JPY'][0])/10), jpy_s="{:.2f}".format(float(fx.get_rate()['JPY'][1])/10))
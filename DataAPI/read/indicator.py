# -*- coding: utf-8 -*-

"""
indicator.py

indicator相关的API

@author: Jasper Gui
@email: jasper.gui@outlook.com
@date: 2018.03.08

-------------------

FUNCTION LIST:
- get_secs_indicator(indicator, sec_ids=[], date='', log=False)
- get_secs_indicator_on_multidays(indicator, sec_ids=[], trading_days=[], log=False)
- get_adjusted_close_price(sec_ids=[], date="")
"""

import os
import traceback

import pandas as pd

from devkit.api import json2dict, Logger, SqliteProxy

from .. config.path import DB_PATH_LIB
from .. utils import classify_dates_by_year
from .. schema import get_schema

from . index_contents import get_index_contents

DB_INDICATOR_PATH = DB_PATH_LIB["indicator"]


def get_secs_indicator(indicator, sec_ids=[], date='', log=False):
    """
    从本地数据库中获取单个日期的单个indicator的值，并返回 DataFrame

    @indicator (str): 单个indicator
    @sec_ids (list): 支持多个股票查询，默认为[]，表示查询范围是全A股
    @date ('%Y-%m-%d'): 单个日期
    @log (Bool): 是否打印log
    :return: Dataframe 列为indicator名，index为sec_id
    """

    if log:
        Logger.info("Reading {} at {}".format(indicator, date), "green")

    if indicator not in get_schema("indicator"):
        Logger.error("Unrecognized indicator: {}".format(indicator))
        raise ValueError

    if not isinstance(sec_ids, list):
        Logger.error("sec_ids must be list!")
        raise ValueError

    if not date:
        Logger.error("Empty date")
        raise ValueError

    if len(sec_ids) == 0: 
        sec_ids = get_index_contents("A", date, False)
    with SqliteProxy(log=log) as proxy:
        path = os.path.join(DB_INDICATOR_PATH, '{}.db'.format(date[:4]))
        proxy.connect(path)

        if len(sec_ids) == 1:
            conds = "sec_id = '{}'".format(sec_ids[0])
        else:
            conds = "sec_id in {}".format(tuple(sec_ids))
        query = "SELECT sec_id, {} FROM [{}] WHERE date = '{}' AND {}".format(indicator, indicator, date, conds)
        try:
            df = proxy.query_as_dataframe(query)
        except Exception:
            Logger.error("Error occurred when reading {} at {}".format(indicator, date))
            traceback.print_exc()
            raise ValueError

        return df.sort_values(by=['sec_id']).set_index(['sec_id'])


def get_secs_indicator_on_multidays(indicator, sec_ids=[], trading_days=[], log=False):
    """
    从本地数据库中获取一段日期的单个indicator的值，并返回 dict of DataFrame

    @indicator (str): 单个indicator
    @sec_ids (list): 支持多个股票查询，默认为[]，表示查询范围是全A股
    @trading_days (["%Y-%m-%d"]): 日期列表
    @log (Bool): 是否打印log
    :return: DataFrame 列为date indicator名，index为sec_id
    """
    if log:
        Logger.info("Reading {} from {} to {}".format(indicator, trading_days[0], trading_days[-1]), "green")

    if indicator not in get_schema("indicator"):
        Logger.error("Unrecognized indicator: {}".format(indicator))
        raise ValueError

    if not isinstance(sec_ids, list):
        Logger.error("sec_ids must be list!")
        raise ValueError

    if not trading_days:
        Logger.error("Empty date")
        raise ValueError

    with SqliteProxy(log=log) as proxy:
        output = {}
        for year, date_list in classify_dates_by_year(trading_days).items():
            path = os.path.join(DB_INDICATOR_PATH, '{}.db'.format(year))
            proxy.connect(path)
            for date in date_list:
                if len(sec_ids) == 0:  # 为空默认全A股
                    conds = ""
                elif len(sec_ids) == 1:
                    conds = "AND sec_id = '{}'".format(sec_ids[0])
                else:
                    conds = "AND sec_id IN {}".format(tuple(sec_ids))
                query = "SELECT sec_id, {} FROM [{}] WHERE date = '{}' {}".format(indicator, indicator, date, conds)
                try:
                    df = proxy.query_as_dataframe(query)
                except Exception:
                    Logger.error("Error occurred when reading {} at {}".format(indicator, date))
                    traceback.print_exc()
                    raise ValueError

                output[date] = df
    df_output = pd.DataFrame()
    for date in output:
        output[date]['date'] = date
        if len(df_output) == 0:
            df_output = output[date]
        else:
            df_output = df_output.append(output[date])

    return df_output


def get_adjusted_close_price(sec_ids=[], date=""):
    """
    从本地数据库中获取某个日期复权后的收盘价，并返回dataframe

    @sec_ids (list): 支持多个股票查询，默认为[],表示查询范围是全A股
    @date ("%Y-%m-%d"): 单个日期 默认为''
    :return: DataFrame，index为sec_id columns为CLOSE (复权后)
    """

    df_close = get_secs_indicator(indicator="CLOSE", sec_ids=sec_ids, date=date, log=False)
    if df_close is None:
        Logger.error("Fail to fetch the close infos on {}".format(date))
        raise ValueError

    df_adjfactor = get_secs_indicator(indicator="ADJFACTOR", sec_ids=sec_ids, date=date, log=False)
    if len(df_adjfactor) == 0:
        Logger.error("Fail to fetch the close infos on {}".format(date))
        raise ValueError

    df_close_adj = pd.DataFrame(df_close['CLOSE'] * df_adjfactor['ADJFACTOR'], columns=['CLOSE'])

    return df_close_adj

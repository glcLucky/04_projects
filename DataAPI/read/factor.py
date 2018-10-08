# -*- coding: utf-8 -*-

"""
factor.py

factor相关的API

@author: Jasper Gui
@email: jasper.gui@outlook.com
@date: 2018.01.09

-------------------

FUNCTION LIST:
- get_secs_factor(factor, sec_ids=[], date="", log=False)
- get_secs_factor_on_multidays(factor, sec_ids=[], trading_days=[], log=False)
"""

import os
import traceback

import pandas as pd

from devkit.api import json2dict, Logger, SqliteProxy

from .. config.path import DB_PATH
from .. utils import classify_dates_by_year
from .. schema import get_schema

from . index_contents import get_index_contents

DB_FACTOR = os.path.join(DB_PATH, "factor")


def get_secs_factor(factor, sec_ids=[], date="", log=False):
    """
    从本地数据库中获取单个日期的单个factor的值，并返回 DataFrame

    @factor (str): 单个factor
    @sec_ids (list): 支持多个股票查询，默认为[]，表示查询范围是全A股
    @date ('%Y-%m-%d'): 单个日期
    @log (Bool): 是否打印log
    :return: Dataframe 列为factor名，index为sec_id
    """

    if log:
        Logger.info("Reading {} at {}".format(factor, date), "green")

    if factor not in get_schema("factor"):
        Logger.error("Unrecognized factor: {}".format(factor))
        raise ValueError

    if not isinstance(sec_ids, list):
        Logger.error("sec_ids must be list!")
        raise ValueError

    if not date:
        Logger.error("Empty date")
        raise ValueError

    with SqliteProxy(log=log) as proxy:
        path = os.path.join(DB_FACTOR, '{}.db'.format(date[:4]))
        proxy.connect(path)

        if len(sec_ids) == 0:  # 为空默认全A股
            conds = ""
        elif len(sec_ids) == 1:
            conds = "AND sec_id = '{}'".format(sec_ids[0])
        else:
            conds = "AND sec_id IN {}".format(tuple(sec_ids))

        query = "SELECT sec_id, {} FROM [{}] WHERE date = '{}' {}".format(factor, factor, date, conds)
        try:
            df = proxy.query_as_dataframe(query)
        except Exception:
            Logger.error("Error occurred when reading {} at {}".format(factor, date))
            traceback.print_exc()
            raise ValueError
        return df.sort_values(by=['sec_id']).set_index(['sec_id'])


def get_secs_factor_on_multidays(factor, sec_ids=[], trading_days=[], log=False):
    """
    从本地数据库中获取一段日期的单个factor的值，并返回 dict of DataFrame

    @factor (str): 单个factor
    @sec_ids (list): 支持多个股票查询，默认为[]，表示查询范围是全A股
    @trading_days (["%Y-%m-%d"]): 日期列表
    @log (Bool): 是否打印log
    :return: {date: Dataframe}，其中 DataFrame 列为factor名，index为sec_id
    """

    if log:
        Logger.info("Reading {} from {} to {}".format(factor, trading_days[0], trading_days[-1]), "green")

    if factor not in get_schema("factor"):
        Logger.error("Unrecognized factor: {}".format(factor))
        raise ValueError

    if not isinstance(sec_ids, list):
        Logger.error("sec_ids must be list!")
        raise ValueError

    if not trading_days:
        Logger.error("Empty date")
        raise ValueError

    # 长连接效率更高，所以这里不是复用 get_secs_factor 而是重新写
    with SqliteProxy(log=log) as proxy:
        output = {}
        for year, date_list in classify_dates_by_year(trading_days).items():
            path = os.path.join(DB_FACTOR, '{}.db'.format(year))
            proxy.connect(path)
            for date in date_list:
                if len(sec_ids) == 0:  # 为空默认全A股
                    conds = ""
                elif len(sec_ids) == 1:
                    conds = "AND sec_id = '{}'".format(sec_ids[0])
                else:
                    conds = "AND sec_id IN {}".format(tuple(sec_ids))
                query = "SELECT sec_id, {} FROM [{}] WHERE date = '{}' {}".format(factor, factor, date, conds)
                try:
                    df = proxy.query_as_dataframe(query)
                except Exception:
                    Logger.error("Error occurred when reading {} at {}".format(factor, date))
                    traceback.print_exc()
                    raise ValueError

                output[date] = df

    return output

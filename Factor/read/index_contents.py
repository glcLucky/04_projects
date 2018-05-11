# -*- coding: utf-8 -*-

"""
index_contents.py
读取指数相关内容

"""

import os
import traceback

import pandas as pd

from devkit.api import json2dict, Logger, MySQLProxy
from .. config import (USER, PASSWORD)


def get_secs_IC(ic_code, trading_days=[], log=False):
    """
    从本地数据库中获取一段日期的单个IC的值，并返回 dict of DataFrame

    @ic_code (str): 单个IC stocks_info: 全A股
    @trading_days (["%Y-%m-%d"]): 日期列表
    @log (Bool): 是否打印log
    :return: {date: Dataframe}，date, sec_id, sec_name, is_st, is_trade, ...
    """

    if log:
        Logger.info("Reading {} from {} to {}".format(ic_code, trading_days[0], trading_days[-1]), "green")

    if not trading_days:
        Logger.error("Empty date")
        raise ValueError

    with MySQLProxy(log=log) as proxy:
        output = {}
        proxy.connect(USER, PASSWORD, 'index')
        #  注： 单个值用=，需要加上引号，多个值用tuple
        if len(trading_days) == 1:
            query = "SELECT * FROM {} WHERE date = '{}' ".format(ic_code, trading_days[0])
        else:
            query = "SELECT * FROM {} WHERE date in {}".format(ic_code, tuple(trading_days))

        try:
            df = proxy.query_as_dataframe(query)
        except Exception:
            Logger.error("Error occurred when reading {} at {}".format(ic_code, date))
            traceback.print_exc()
            raise ValueError

    return df

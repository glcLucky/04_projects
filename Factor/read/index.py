# -*- coding: utf-8 -*-

"""
index.py

index相关的API

@author: Jasper Gui
@email: jasper.gui@outlook.com
@date: 2018.03.08

-------------------

FUNCTION LIST:
- get_secs_index(index, sec_ids=[], date='', log=False)
- get_secs_index_on_multidays(index, sec_ids=[], trading_days=[], log=False)
- get_adjusted_close_price(sec_ids=[], date="")
"""

import os
import traceback
import gc
import pandas as pd

from devkit.api import (
    json2dict,
    Logger,
    MySQLProxy,
    get_tables_on_given_database,
)

from .. config import (USER, PASSWORD)
from .. schema import get_schema


def get_secs_index(index, sec_ids=[], trading_days=[], log=False):
    """
    从本地数据库中获取一段日期的单个index的值，并返回 dict of DataFrame

    @index (str): 单个index
    @sec_ids (list): 支持多个股票查询，默认为[]，表示查询范围是全A股
    @trading_days (["%Y-%m-%d"]): 日期列表
    @log (Bool): 是否打印log
    :return: {date: Dataframe}，其中 DataFrame 列为index名，index为sec_id
    """

    if log:
        Logger.info("Reading {} from {} to {}".format(index, trading_days[0], trading_days[-1]), "green")

    # if index not in get_schema("index"):
    #     Logger.error("Unrecognized index: {}".format(index))
    #     raise ValueError

    if not isinstance(sec_ids, list):
        Logger.error("sec_ids must be list!")
        raise ValueError

    if not trading_days:
        Logger.error("Empty date")
        raise ValueError

    with MySQLProxy(log=log) as proxy:
        output={}
        proxy.connect(USER, PASSWORD, "index")
        #  注： 单个值用=，需要加上引号，多个值用tuple
        if len(sec_ids) == 0:
            if len(trading_days) == 1:
                query="SELECT * FROM {} WHERE date = '{}' ".format(index, trading_days[0])
            else:
                query="SELECT * FROM {} WHERE date in {}".format(index, tuple(trading_days))
        elif len(sec_ids) == 1:
            if len(trading_days) == 1:
                query="SELECT * FROM {} WHERE date = '{}' AND sec_id = '{}' ".format(index, trading_days[0], sec_ids[0])
            else:
                query="SELECT * FROM {} WHERE date in {} AND sec_id = '{}' ".format(index, tuple(trading_days), sec_ids[0])
        else:
            if len(trading_days) == 1:
                query="SELECT * FROM {} WHERE date = '{}' AND sec_id in {}".format(index, trading_days[0], tuple(sec_ids))
            else:
                query="SELECT * FROM {} WHERE date in {} AND sec_id in {}".format(index, tuple(trading_days), tuple(sec_ids))

        try:
            df=proxy.query_as_dataframe(query)
        except Exception:
            Logger.error("Error occurred when reading {} ".format(inde))
            traceback.print_exc()
            raise ValueError
    df['date']=df['date'].apply(lambda x: str(x))
    return df


def get_secs_index_std(index_std, sec_ids=[], trading_days=[], log=False):
    """
    从本地数据库中获取一段日期的单个index_std的值，并返回 DataFrame

    @index_std (str): 单个index_std
    @sec_ids (list): 支持多个股票查询，默认为[]，表示查询范围是全A股
    @trading_days (["%Y-%m-%d"]): 日期列表
    @log (Bool): 是否打印log
    :return: {date: Dataframe}，其中 DataFrame 列为index_std名，index_std为sec_id
    """

    if log:
        Logger.info("Reading {} from {} to {}".format(index_std, trading_days[0], trading_days[-1]), "green")

    # if index_std not in get_schema("index_std"):
    #     Logger.error("Unrecognized index_std: {}".format(index_std))
    #     raise ValueError

    if not isinstance(sec_ids, list):
        Logger.error("sec_ids must be list!")
        raise ValueError

    if not trading_days:
        Logger.error("Empty date")
        raise ValueError

    with MySQLProxy(log=log) as proxy:
        output={}
        proxy.connect(USER, PASSWORD, "index_std")
        #  注： 单个值用=，需要加上引号，多个值用tuple
        if len(sec_ids) == 0:
            if len(trading_days) == 1:
                query="SELECT * FROM {} WHERE date = '{}' ".format(index_std, trading_days[0])
            else:
                query="SELECT * FROM {} WHERE date in {}".format(index_std, tuple(trading_days))
        elif len(sec_ids) == 1:
            if len(trading_days) == 1:
                query="SELECT * FROM {} WHERE date = '{}' AND sec_id = '{}' ".format(index_std, trading_days[0], sec_ids[0])
            else:
                query="SELECT * FROM {} WHERE date in {} AND sec_id = '{}' ".format(index_std, tuple(trading_days), sec_ids[0])
        else:
            if len(trading_days) == 1:
                query="SELECT * FROM {} WHERE date = '{}' AND sec_id in {}".format(index_std, trading_days[0], tuple(sec_ids))
            else:
                query="SELECT * FROM {} WHERE date in {} AND sec_id in {}".format(index_std, tuple(trading_days), tuple(sec_ids))

        try:
            df=proxy.query_as_dataframe(query)
        except Exception:
            Logger.error("Error occurred when reading {} ".format(inde))
            traceback.print_exc()
            raise ValueError
    df['date']=df['date'].apply(lambda x: str(x))
    return df


def get_secs_multiple_index_stds(index_stds=[], sec_ids=[], trading_days=[], log=False):
    """
    从本地数据库中获取一段日期的多index_std的值，并返回 DataFrame

    @index_stds (list): 多个index_std
    @sec_ids (list): 支持多个股票查询，默认为[]，表示查询范围是全A股
    @trading_days (["%Y-%m-%d"]): 日期列表
    @log (Bool): 是否打印log
    :return: {date: Dataframe}，其中 DataFrame 列为index_std名，index_std为sec_id
    """

    if len(index_stds) == 0:
        index_stds = get_tables_on_given_database(USER, PASSWORD, 'index_std')
    output = pd.DataFrame()
    for index_std in index_stds:
        a = get_secs_index_std(index_std, sec_ids, trading_days, log)
        a = a[['date', 'sec_id', index_std]]
        if len(output) == 0:
            output = a.copy()
        else:
            output = output.merge(a, how='inner', on=['date', 'sec_id'])
        del a
        gc.collect()
    return output


def get_secs_multiple_indexs(indexs=[], sec_ids=[], trading_days=[], log=False):
    """
    从本地数据库中获取一段日期的多index_std的值，并返回 DataFrame
    @indexs (list): 多个index_std
    @sec_ids (list): 支持多个股票查询，默认为[]，表示查询范围是全A股
    @trading_days (["%Y-%m-%d"]): 日期列表
    @log (Bool): 是否打印log
    :return: {date: Dataframe}，其中 DataFrame 列为index_std名，index_std为sec_id
    """

    if len(indexs) == 0:
        indexs = get_tables_on_given_database(USER, PASSWORD, 'index')
    output = pd.DataFrame()
    for index in indexs:
        a = get_secs_index(index, sec_ids, trading_days, log)
        a = a[['date', 'sec_id', index]]
        if len(output) == 0:
            output = a.copy()
        else:
            output = output.merge(a, how='outer', on=['date', 'sec_id'])
        del a
        gc.collect()
    return output


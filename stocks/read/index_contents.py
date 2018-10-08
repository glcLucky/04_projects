# -*- coding: utf-8 -*-

"""
index_contents.py

读取指数成分股的API

@author: Jasper Gui
@email: jasper.gui@outlook.com
@date: 2018.03.13

-------------------

FUNCTION LIST:
- get_index_contents(index_code, date="", approx=False, log=False)
- get_index_contents_from_sql(index_code, date="", log=False)
- get_index_contents_from_csv(index_code)
- get_index_contents_on_multidays(index_code, trading_days=[], log=False)
- get_secs_name(sec_ids=[])
- get_secs_name_from_sql(sec_ids=[], index_code="A")
- get_secs_name_from_csv(sec_ids=[], index_code="H")
- get_index_weights(index_code, date="")
"""

import os
import traceback

from devkit.api import SqliteProxy, Logger, open_csv_as_df
from finkit.api import classify_equity, get_nearest_trading_day

from .. config.path import DB_PATH_LIB
from .. schema import get_schema
from .. utils import classify_dates_by_year

DB_INDEX_CONTENTS = DB_PATH_LIB['index_contents']
IDXCONT_AS_SQL = ("A", "000016.SH", "000300.SH", "000905.SH")
IDXCONT_AS_CSV = ("H", "HSI.HI")


def get_index_contents(index_code, date="", approx=False, log=False):
    """
    读取单个日期指数成分股列表

    @index_code (str): 指数代码，目前支持 ['A', 'H', '000905.SH', '000300.SH', '000016.SH', 'HSI.HI']
    @date ('%Y-%m-%d'): 单个日期
    @log (Bool): 是否打印log
    :return (list): 股票代码列表
    """

    if log:
        Logger.info("Reading index contents of {} on {}".format(index_code, date), "green")

    if not date:
        Logger.error("Empty date")
        raise ValueError

    # approx 用于保证更新 indicator 财报数据时财报日非交易日的情况
    if approx:
        date = get_nearest_trading_day(date=date, direction='left', self_included=True)

    if index_code in IDXCONT_AS_SQL:
        output = get_index_contents_from_sql(index_code, date, log=log)
    elif index_code in IDXCONT_AS_CSV:
        output = get_index_contents_from_csv(index_code)
    else:
        Logger.error("Unrecognized index code: {}".format(index_code))
        raise ValueError
    return output


def get_index_contents_from_sql(index_code, date="", log=False):
    path = os.path.join(DB_INDEX_CONTENTS, '{}.db'.format(date[:4]))
    with SqliteProxy(log=log) as proxy:
        proxy.connect(path)
        query = "SELECT sec_id FROM [{}] WHERE date = '{}'".format(index_code, date)
        try:
            df = proxy.query_as_dataframe(query)
        except Exception:
            Logger.error("Error occurred when reading {} at {}".format(index_code, date))
            traceback.print_exc()
            raise ValueError

    if len(df) == 0:
        Logger.warn("Empty result when reading {} at {}".format(index_code, date))
        return []

    return df["sec_id"].tolist()


def get_index_contents_from_csv(index_code):
    path = os.path.join(DB_INDEX_CONTENTS, '{}.csv'.format(index_code))
    info = open_csv_as_df(path, validate=False)
    return info["sec_id"].tolist()


def get_index_contents_on_multidays(index_code, trading_days=[], log=False):
    """
    读取多个日期某指数全部股票列表

    @index_code (str): 指数代码，目前支持 ['A', '000905.SH', '000300.SH', '000016.SH']
    @trading_days (['%Y-%m-%d']): 日期列表
    @log (Bool): 是否打印log
    :return: ({date: list}), key为date value为 股票代码列表
    """

    if log:
        Logger.info("Reading all {} records between trading_days ...".format(index_code), "green")

    if len(trading_days) == 0:
        Logger.error("Empty date")
        raise ValueError
    elif len(trading_days) == 1:
        date = trading_days[0]
        return {date: get_index_contents(index_code, date, log=False)}

    output = {}
    if index_code in IDXCONT_AS_SQL:
        with SqliteProxy(log=log) as proxy:
            for year, date_list in classify_dates_by_year(trading_days).items():
                path = os.path.join(DB_INDEX_CONTENTS, '{}.db'.format(year))
                proxy.connect(path)

                query = "SELECT date, sec_id FROM [{}] WHERE date IN {}".format(index_code, tuple(date_list))
                try:
                    df = proxy.query_as_dataframe(query)
                except Exception:
                    Logger.error("Empty result when reading {} from {} to {}".format(
                        index_code, trading_days[0], trading_days[-1]
                    ))
                    traceback.print_exc()
                    raise ValueError

                if len(df) == 0:
                    Logger.warn("Empty result when reading {} from {} to {}".format(
                        index_code, trading_days[0], trading_days[-1]
                    ))

                for date in date_list:
                    output[date] = df[df.date == date]['sec_id'].tolist()
    elif index_code in IDXCONT_AS_CSV:
        info = get_index_contents_from_csv(index_code)
        output = {date: info for date in trading_days}
    else:
        Logger.error("Unrecognized index code: {}".format(index_code))
        raise ValueError
    return output


def get_secs_name(sec_ids=[]):
    """
    获取最新日期股票名称，自动处理A股和H股，数据格式为 {股票代码：股票名称}

    @sec_id (list): 股票列表 默认为空 表示最新日期的所有A股和H股
    :return: {sec_id: sec_name}
    """

    classifier = classify_equity(sec_ids)
    output = {}

    if classifier["A股"]:
        output.update(get_secs_name_from_sql(classifier["A股"], "A"))

    if classifier["港股"]:
        output.update(get_secs_name_from_csv(classifier["港股"], "H"))

    if classifier["其他"]:
        Logger.warn("Unrecognized sec_ids: {}".format(classifier["其他"]))

    return output


def get_secs_name_from_sql(sec_ids=[], index_code="A"):
    """
    获取最新日期A股或港股股票名称，数据格式为 {股票代码：股票名称}

    @sec_id (list): 股票列表 默认为空 表示最新日期的所有A股
    @index_code (str): 数据库名称
    :return: {sec_id: sec_name}
    """

    last_date = get_schema('index_contents')[index_code]['end date']

    dbpath = os.path.join(DB_INDEX_CONTENTS, '{}.db'.format(last_date[:4]))
    with SqliteProxy(log=False) as proxy:
        proxy.connect(dbpath)
        if len(sec_ids) == 0:  # 默认取所有股票
            query = "SELECT sec_id, sec_name FROM [{}] WHERE date = '{}'".format(
                index_code, last_date)
        elif len(sec_ids) == 1:
            query = "SELECT sec_id, sec_name FROM [{}] WHERE date = '{}' AND sec_id = '{}'".format(
                index_code, last_date, sec_ids[0])
        else:
            query = "SELECT sec_id, sec_name FROM [{}] WHERE date = '{}' AND sec_id in {}".format(
                index_code, last_date, tuple(sec_ids))
        df = proxy.query_as_dataframe(query).set_index("sec_id")

        if len(df) == 0:
            Logger.warn("Empty result for query contents from {} on {}".format(index_code, last_date))

        output = {sec: df.at[sec, "sec_name"] for sec in sec_ids if sec in df.index}
        return output


def get_secs_name_from_csv(sec_ids=[], index_code="H"):
    path = os.path.join(DB_INDEX_CONTENTS, '{}.csv'.format(index_code))
    df = open_csv_as_df(path, validate=False).set_index("sec_id")
    output = {sec: df.at[sec, "sec_name"] for sec in df.index}
    if not sec_ids:
        return output
    else:
        return {sec: name for sec, name in output.items() if sec in sec_ids}


def get_index_weights(index_code, date=""):
    """
    读取单个日期指数成分股的权重

    @index_code (str): 指数代码，目前支持 ['000016.SH', '000300.SH', '000905.SH']
    @date (%Y-%m-%d): 单个日期
    :return: {sec_id: weight}
    """

    if not date:
        Logger.error("Empty date")
        raise ValueError

    if index_code not in ['000016.SH', '000300.SH', '000905.SH']:
        Logger.error("Invalid index code: {}".format(index_code))

    dbpath = os.path.join(DB_INDEX_CONTENTS, '{}.db'.format(date[:4]))
    with SqliteProxy(log=False) as proxy:
        proxy.connect(dbpath)
        query = "SELECT sec_id, weight FROM [{}] WHERE date = '{}' ".format(index_code, date)
        df = proxy.query_as_dataframe(query)

        if len(df) == 0:
            Logger.warn("Empty result when reading {} at {}".format(index_code, date))
            output = {}
        else:
            output = {df.at[i, 'sec_id']: df.at[i, 'weight'] for i in range(len(df))}

        return output

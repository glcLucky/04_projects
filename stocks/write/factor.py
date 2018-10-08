# -*- coding: utf-8 -*-

"""
factor.py
写入因子原始数据

@author: Jasper Gui
@email: jasper.gui@outlook.com
@date: 2017.12.29

-------------------

FUNCTION LIST:
- update_single_factor(factor, trading_days=[], override=False, log=False)
- update_factors(factors=[], trading_days=[], override=False, log=False)
"""

import os
import traceback

from devkit.api import json2dict, Logger, SqliteProxy

from .. config.path import DB_PATH
from .. load import load_single_factor_on_single_day
from .. utils import classify_dates_by_year
from .. schema import get_schema, update_schema

from .. utils import create_table

DB_FACTOR = os.path.join(DB_PATH, "factor")


def update_single_factor(factor, trading_days=[], override=False, log=False):
    """
    更新单个factor的指定日期列表的数据

    @factor (str): factor名称
    @trading_days ([%Y-%m-%d]): 日期列表
    @override (Bool): 是否覆盖原记录，默认为False，表示不覆盖
    @log (Bool): 是否打印log
    """

    Logger.info("Updating factor {}".format(factor), "green")

    _n_updated_date = 0

    if factor not in get_schema('factor'):
        Logger.error("Unrecognized factor: {}".format(factor))
        raise ValueError

    if not trading_days:
        Logger.error("Empty date")
        raise ValueError

    with SqliteProxy(log=log) as proxy:
        date_classfier = classify_dates_by_year(trading_days)

        for year, date_list in date_classfier.items():
            path = os.path.join(DB_FACTOR, '{}.db'.format(year))
            proxy.connect(path)

            if factor not in proxy.list_tables:
                create_table(proxy, "factor", factor)

            # 判断已有数据
            if len(date_list) == 1:
                query = "SELECT DISTINCT(date) FROM {} WHERE date = '{}'".format(factor, date_list[0])
            else:
                query = "SELECT DISTINCT(date) FROM {} WHERE date in {}".format(factor, tuple(date_list))
            lookup = proxy.query_as_dataframe(query)
            lookup = set(lookup['date'].tolist())

            for date in date_list:
                if date in lookup and not override:  # 更新的日期已经存在于数据库时，不覆盖则跳过
                    if log:
                        Logger.warn("{} records on {} is existed.".format(factor, date))
                    continue

                try:
                    df = load_single_factor_on_single_day(factor=factor, date=date)
                except Exception:
                    Logger.error("Error occurred when loading {} on {}".format(factor, date))
                    traceback.print_exc()
                    continue

                if df is not None:  # 从Wind下载数据成功时
                    if date in lookup and override:  # 覆盖时删除原记录
                        proxy.execute("DELETE FROM [{}] WHERE date = '{}'".format(factor, date))

                    df['date'] = date
                    try:
                        proxy.write_from_dataframe(df, factor)
                    except Exception:
                        Logger.error("Error occurred when writing {} on {}".format(factor, date))
                        traceback.print_exc()
                        raise ValueError

                    if log:
                        Logger.info("{} on {} is updated successfully".format(factor, date))
                    _n_updated_date += 1
                else:  # 从wind提取数据失败时
                    Logger.error("Fail to fetch {} data on {}".format(factor, date))
                    raise ValueError

    update_schema(db_name="factor", sub_name=factor)

    if log:
        _n_all_date = len(trading_days)
        _n_existed_date = _n_all_date - _n_updated_date
        Logger.info("传入日期数：{}  已经存在个数：{}  实际写入次数：{}".format(
            _n_all_date, _n_existed_date, _n_updated_date
        ))
        Logger.info("factor {} is updated.".format(factor), color="green")
        Logger.info("------------------------------------------")


def update_factors(factors=[], trading_days=[], override=False, log=False):
    """
    更新多个factor的指定日期列表的数据

    @factors (<list>):factor名称构成的列表
    @trading_days ([%Y-%m-%d]): 日期列表
    @override (<Bool>): 是否覆盖原记录 默认为False 表示不覆盖
    @log (<Bool>): 是否打印log
    """

    SCHEMA = get_schema("factor")
    if not factors:
        factors = sorted(SCHEMA, key=lambda x: SCHEMA[x]["level"])

    for fac in factors:
        if fac in SCHEMA:
            update_single_factor(factor=fac, trading_days=trading_days, override=override, log=log)
        else:
            Logger.error("Unrecognized factor: {}".format(fac))
            Logger.info("------------------------------------------")

# -*- coding: utf-8 -*-

"""
indicator.py

写入指标原始数据

@author: Gui lichao
@email:
@date: 2018.01.15

-------------------

FUNCTION LIST:
- update_factor_return_data
"""

import os
import pandas as pd

from devkit.api import json2dict, Logger
from finkit.datetime_utils.utils import normalize

from .. utils import get_date_lists_in_table
from .. config.path import DB_PATH
from .. config.path import DB_PATH_LIB
from .. load.factor_return import load_single_factor_return_on_multidays
from .. schema import (
    get_schema,
    update_factor_return_schema,
)


def update_single_factor_return(factor_return, trading_days=[], group_num=10, log=True):
    """
    根据trading_days更新factor_return数据

    @factor_return (<str>): factor的名称
    @trading_days (<[%Y-%m-%d]>) : 日期列表
    @group_num (<int>): 分组个数
    """

    if log:
        Logger.info("Updating factor_return {}...".format(factor_return))

    if factor_return not in get_schema("factor_return"):
        Logger.error("Unrecognized factor_return: {}".format(factor_return))
        return
    factor_path = DB_PATH_LIB['factor']
    factor_exist_dates = get_date_lists_in_table(factor_path, factor_return)
    not_found_date = list(set(trading_days) - set(factor_exist_dates))
    if len(not_found_date) != 0 and log:
        Logger.warn("Fail to update these factor returns on following dates due to lack factor:{}".format(not_found_date))

    trading_days = list(set(trading_days) - set(not_found_date))
    if len(trading_days) == 0:
        Logger.error("No valid date to update")
        return

    trading_days = sorted(trading_days)
    db_factor_return_path = os.path.join(DB_PATH, "factor_return")
    filepath = os.path.join(db_factor_return_path, '{}.csv'.format(factor_return))
    df_new = load_single_factor_return_on_multidays(factor_return, trading_days, group_num)

    _n_updated_date = len(df_new)

    if not os.path.exists(filepath):  # 没有已经更新过的记录
        Logger.info("首次更新 {}数据".format(factor_return))
        output = df_new.copy()
        output.to_csv(filepath, encoding="utf-8")
    else:
        df_old = pd.read_csv(filepath, encoding="utf-8")  # 已经存在的所有return数据
        min_exist_date = normalize(df_old['date'].min(), "%Y-%m-%d")
        max_exist_date = normalize(df_old['date'].max(), "%Y-%m-%d")
        max_update_date = trading_days[-1]
        min_update_date = trading_days[1]  # 因为只能第二个日期才能计算收益

        if (max(min_update_date, max_update_date) < min_exist_date) or \
           (min(min_update_date, max_update_date) > max_exist_date):
            Logger.error("非法更新：待更新时间段孤立于现有的时间段")
            Logger.error("开始更新日期：{}  结束更新日期：{}".format(
                min_update_date, max_update_date))
            Logger.error("原有开始日期：{}  原有结束日期：{}".format(
                min_exist_date, max_exist_date))
            return

        if (min_update_date < min_exist_date) and \
           (max_update_date <= max_exist_date) and \
           (max_update_date >= min_exist_date):
            Logger.info("左更新：更新之前记录")

        if (min_update_date >= min_exist_date) and (max_update_date <= max_exist_date):
            Logger.info("存量更新：更新当前已经有的记录")

        if (min_update_date >= min_exist_date) and \
           (min_update_date <= max_exist_date) and \
           (max_update_date > max_exist_date):
            Logger.info("右更新：更新未来的记录")

        if (min_update_date < min_exist_date) and \
           (max_update_date > max_exist_date):
            Logger.info("全更新：当前已经存在的日期是待更新日期的子集")

        df_old['date'] = df_old['date'].apply(
            lambda x: normalize(x, "%Y-%m-%d"))
        df_new['date'] = df_new['date'].apply(
            lambda x: normalize(x, "%Y-%m-%d"))
        bool_list = df_old['date'].isin(df_new['date']).apply(
            lambda x: not x)  # 旧数据不在更新日期中为True
        # 取出那些不在本次更新范围内但原数据已经存在的日期列表 这些日期直接copy 无需计算
        df_old = df_old[bool_list]
        output = df_old.append(df_new).sort_values(by=['date'])

    output = output.set_index(['date'])
    format_var_name_list = ['group{:0>2}'.format(
        i) for i in range(1, group_num + 1)]
    format_var_name_list.append('{}'.format(factor_return))
    output = output.reindex(columns=format_var_name_list)
    output.to_csv(filepath, encoding="utf-8")

    update_factor_return_schema(factor_return)
    if log:
        _n_all_date = len(output)
        _n_existed_date = _n_all_date - _n_updated_date

        Logger.info("传入日期数：{}  已经存在个数：{}  实际写入次数：{}".format(
            _n_all_date, _n_existed_date, _n_updated_date
        ))
        Logger.info("factor_return {} is updated.".format(factor_return), color="green")
        Logger.info("------------------------------------------")


def update_factors_return(factors_ret_to_update=[], trading_days=[], group_num=10, log=True):
    """
    根据trading_days更新factor_return数据

    @factors_ret_to_update (<list>):  factor列表
    @trading_days (<[%Y-%m-%d]>) : 日期列表
    @group_num (<int>): 分组个数
    @log (<Bool>): 是否打印log
    """
    factor_return_schema = get_schema('factor_return')
    if len(factors_ret_to_update) == 0:
        factors_ret_to_update = list(factor_return_schema.keys())

    for factor_ret in factors_ret_to_update:
        if factor_ret not in factor_return_schema:
            Logger.error("Unrecognized factor return: {}".format(factor_ret))
        else:
            update_single_factor_return(factor_ret, trading_days, group_num, log)

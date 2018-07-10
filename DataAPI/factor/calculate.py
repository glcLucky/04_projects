# -*- coding: utf-8 -*-

"""
calculate_factors.py

储存计算每个因子的函数  形如calculate_XX XX为某因子

@author: Wu Yudi
@email: jasper.wuyd@gmail.com
@date: 2018.03.08

-------------------
分析思路：
1、基于必要的indicator计算factor

2、将factor分为缺失集合非缺失集两部分（mark_missing）分别为missing和non_missing，missing的factor设为0.0

3、将non_missing部分进行winsorize，下确界：0.01 上确界：0.99
    返回三个部分，即正常值部分：normal_sector 极小部分：lower_sector 极大部分：upper_sector

4、基于normal_sector数据求均值和标准差，并进行统计标准化（standardize）

5、将位于下确界以下的因子值赋为标准化后normal_sector的因子值的最小值
   将位于上确界以上的因子值赋为normal_standardize_sector的因子值的最大值

6、将缺失集missing、极端值lower_sector和upper_sector以及标准化后的正常部分normal_sector
    纵向拼在一起，得到处理后的FACTOR，记为FACTOR_final

7、返回FACTOR_final
-------------------

FUNCTION LIST:

"""

import inspect

import pandas as pd

from devkit.api import Logger

from .. config import DB_PATH_LIB
from .. read import (
    get_index_contents,
    get_secs_indicator,
    get_secs_factor,
)
from .. schema import get_schema
from .. utils import (
    get_previous_report_day,
    get_previous_existed_day_in_table,
    statistical_process,
    get_date_lists_in_table,
)

from . import formula
from . const import (
    WINSORIZE_LB,
    WINSORIZE_UB,
    MISSING_CRITERION,
)

DB_FACTOR = DB_PATH_LIB['factor']
INDICATOR_SCHEMA = get_schema("indicator")


def load_context(factor, date):
    schema = get_schema("factor")[factor]
    varlist = schema['context']
    universe = get_index_contents("A", date, False)
    if universe is None:
        Logger.error("Fail to fetch stock lists in following dates: {}".format(date))
        raise ValueError
    df_today = pd.DataFrame(universe, columns=['sec_id'])  # 获取当天全A股列表
    last_report_day = get_previous_report_day(date)  # 供可能的indicator使用
    context = df_today.copy()
    missing_flag = 0  # 缺失过度标志
    for indicator, lags in varlist["indicators"].items():
        if INDICATOR_SCHEMA[indicator]["type"] == "财报数据":
            date = last_report_day

        if len(lags) == 1 and lags[0] == 0:
            selected_date = [date]
        else:
            existed_date = get_date_lists_in_table(DB_PATH_LIB['indicator'], indicator)
            selected_date = [ins for ins in existed_date if ins <= date]
            selected_date = sorted(selected_date, reverse=True)
        for lag in lags:
            var_name = indicator
            ind_date = selected_date[lag]
            df_context = get_secs_indicator(indicator=indicator, date=ind_date, log=False)
            if lag > 0:
                var_name = "{}_{}".format(indicator, lag)
                df_context = df_context.rename(columns={indicator: var_name})

            context = context.merge(df_context, how="left", left_on='sec_id', right_index=True)
            if (context[indicator].isnull().sum() / context.shape[0]) > MISSING_CRITERION:
                missing_flag = 1
                break
            ind_date = ''
            df_context = None
        if missing_flag == 1:
            break

    if not missing_flag:
        for factor, lags in varlist["factors"].items():
            if len(lags) == 1 and lags[0] == 0:
                selected_date = [date]
            else:
                existed_date = get_date_lists_in_table(DB_FACTOR, factor)
                selected_date = [ins for ins in existed_date if ins <= date]
                selected_date = sorted(selected_date, reverse=True)
            for lag in lags:
                var_name = factor
                ind_date = selected_date[lag]
                df_context = get_secs_factor(factor=factor, date=ind_date, log=False)
                if lag > 0:
                    var_name = "{}_{}".format(factor, lag)
                    df_context = df_context.rename(columns={factor: var_name})

                context = context.merge(df_context, how="left", left_on='sec_id', right_index=True)
                if (context[var_name].isnull().sum() / context.shape[0]) > MISSING_CRITERION:
                    missing_flag = 1
                    break
                ind_date = ''
                df_context = None

            if missing_flag == 1:
                break
    return context, df_today, missing_flag


def calculate_factor(factor, date):
    """
    通过对indicator的计算得到因子的值

    :param: factor (str): 该factor的名字
    :param: date (%Y-%m-%d): 日期
    :return: dataframe 处理后的因子值
    """
    func = getattr(formula, "calculate_raw_{}".format(factor))
    if func is None:
        Logger.error("Formula not implemented: {}".format(factor))
        raise ValueError
    context, df_today, missing_flag = load_context(factor, date)
    last_day = get_previous_existed_day_in_table(date, DB_FACTOR, factor)
    if missing_flag == 1:
        if last_day is None:  # 无最新数据
            Logger.error("当前日期数据缺失值太多，且之前没有可以复制的文件")
            raise ValueError
        else:
            Logger.warn("由于 {} 值缺失太多直接复制于 {}".format(date, last_day))
            try:
                df_last = get_secs_factor(factor, sec_ids=[], date=last_day, log=False)
            except Exception:
                traceback.print_exc()
                Logger.warn("无法提取 {} 上个记录日的数据".format(factor))
                raise ValueError
            value = df_today.merge(df_last, how="left", left_on='sec_id', right_index=True)
            return value
    else:
        data_raw = func(context)
        data_final = statistical_process(  # 数据处理: 缺失值分离 winsorize 标准化
            data=data_raw,
            var=factor,
            winsor_LB=WINSORIZE_LB,
            winsor_UB=WINSORIZE_UB
        )
        return data_final

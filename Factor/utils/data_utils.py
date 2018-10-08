# -*- coding: utf-8 -*-

"""
data_utils.py

数据处理工具函数

@author: Jasper Gui
@email: jasper.gui@outlook.com
@date: 2018.03.08

-------------------

FUNCTION LIST:
- mark_missing
- winsorize
- standardize
- statistical_process
"""

import os
import traceback
import gc
import pandas as pd
from scipy import stats
from datetime import datetime

from devkit.api import Logger
from .. read import get_secs_index


def process_ts_index(index, trading_days, cp=3):
    """
    给定trading_days列表，处理原始指标 包括剔除当天停牌股、st股，统计标准化，剔除cp倍标准差之外的样本
    @index <str>: 指标名称
    @trading_days <list of str>: 交易日列表
    @cp <float>: critical point 极端值处理的阈值  默认为3
    """

    output = pd.DataFrame()
    df_ic = get_secs_index("stocks_info", [], trading_days)
    index_raw = get_secs_index(index, [], trading_days)
    for date in trading_days:
        print(date)
        temp = pd.DataFrame()
        df_ic1 = df_ic[df_ic.date == date]
        conds = (df_ic1.is_trade == 1).multiply(df_ic1.is_st == 0)
        df_ic2 = df_ic1[conds]
        sec_ids = df_ic2.sec_id.tolist()
        temp1 = get_secs_index(index, sec_ids, [date])
        if len(temp1) != 0:
            temp1[index] = (temp1[index] - temp1[index].mean()) / temp1[index].std()  # 统计标准化
            temp2 = temp1[temp1[index].abs() <= cp]  # 删除极端值
            output = output.append(temp2)
        else:
            continue
        del temp, temp1, temp2, df_ic1, df_ic2, sec_ids
        gc.collect()
    del df_ic, index_raw
    gc.collect()
    output = output.rename(columns={index: "{}_std".format(index)})
    output = output.dropna()
    return output


def paired_ttest(data):
    """
    配对t检验
    @data <DataFrame>: 包含两列的DataFrame 该两列是将进行配对检验的数据
    """

    return stats.ttest_rel(data.iloc[:, 0], data.iloc[:, -1])


def report_map_to_trade_day(index):
    """
    根据当前close已有的日期确定dummy 然后根据以下规则确定对应日期可获得的最新报告日
    2010-01-01 -- 2010-04-31 取上年三季报 即 date_report = 2009-09-30
    2010-05-01 -- 2010-07-31 取上年年报   即 date_report = 2009-12-31
    2010-08-01 -- 2010-09-30 取本年一季报 即 date_report = 2010-03-31
    2010-10-01 -- 2010-10-31 取本年中报   即 date_report = 2010-06-30
    2010-11-01 -- 2010-12-31 取本年三季报 即 date_report = 2010-09-30
    """
    conn = dk.MySQLProxy()
    conn.connect('root', '123888', 'index')
    dummy = conn.query_as_dataframe("SELECT date, sec_id FROM close")
    dummy['date_report'] = dummy.date

    def date2report(x):
        if 1 <= x.month <= 4:
            x = datetime(x.year - 1, 9, 30).date()
        elif 5 <= x.month <= 7:
            x = datetime(x.year - 1, 12, 31).date()
        elif 8 <= x.month <= 9:
            x = datetime(x.year, 3, 31).date()
        elif x.month == 10:
            x = datetime(x.year, 6, 30).date()
        elif 11 <= x.month <= 12:
            x = datetime(x.year, 9, 30).date()
        else:
            print("Invalid date!!")
        return x
    dummy['date_report'] = dummy.date_report.apply(lambda x: date2report(x))
    dummy = dummy.rename(columns={'date_report': 'date_report_available'})
    return dummy

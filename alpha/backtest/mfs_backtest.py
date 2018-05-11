# -*- coding: utf-8 -*-

"""
mfs_backtest.py
多因子选股模型回测框架

@author: Gui lichao
@date: 2018-04-20

"""

import pandas as pd
from Factor.read import (
    get_secs_index,
)
import finkit.api as fk
import devkit.api as dk


def calculate_period_return(start, end, sec_id=[], price_type='close'):
    """
    @sec_id <list>: 股票列表
    @price_type <str>: 价格类型 close open high low
    """
    a = get_secs_index(index=price_type, sec_ids=sec_id, trading_days=[start])
    a = a[['sec_id', price_type]].rename(columns={price_type: price_type + '_start'})
    b = get_secs_index(index=price_type, sec_ids=sec_id, trading_days=[end])
    b = b[['sec_id', price_type]].rename(columns={price_type: price_type + '_end'})
    c = a.merge(b, on=['sec_id'])
    d = c['{}_end'.format(price_type)].sum() / c['{}_start'.format(price_type)].sum() - 1
    return d


def back_test_on_given_model(start_date, end_date, cycle, windows, num, model, benchmark="000300.SH"):
    """
    根据给定的mfs模型在指定时间段内按指定换仓周期进行回测
    @start_date <"%Y-%m-%d">: 回测开始日期
    @end_date <"%Y-%m-%d">: 回测结束日期
    @cycle <int>: 换仓周期
    @windows <int>: 计算因子权重的滚动窗口 即根据近多少个交易日进行分组有效性检验
    @num <int>: 持股个数
    @model <function>: 选股模型函数 可选： mfs_by_score
    @benchmark <str>: 基准 hs300
    """

    output = {}
    trading_days = fk.get_trading_days(start_date, end_date)
    start = start_date  # 初始建仓点
    while (trading_days.index(start) + cycle) < len(trading_days):  # 当建仓后cycle个交易日后有值时执行
        end = trading_days[trading_days.index(start) + cycle]
        print(start)
        selected_stocks = model(date=start, windows=windows, num=num)
        # 获取开始日期和结束日期的收盘价
        model_return = calculate_period_return(start, end, selected_stocks)
        bench_return = calculate_period_return(start, end, [benchmark])
        output[start] = {"model_return": model_return, "hs_300_return": bench_return}
        if trading_days.index(end) + 1 >= len(trading_days):
            break
        start = trading_days[trading_days.index(end) + 1]
    df = pd.DataFrame(output).T
    df1 = df.copy()
    for i in range(df.shape[0]):
        if i == 0:
            df1.iloc[i, :] = 1
        else:
            df1.iloc[i, :] = df1.iloc[i - 1, :] + df.iloc[i, :]
    return output


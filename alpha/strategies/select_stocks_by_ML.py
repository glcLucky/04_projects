# -*- coding: utf-8 -*-

"""
select_stocls_by_ML.py
基于机器学习方法的多因子选股模型

思路:
1. 基于财务指标选出具有长期收益的股票作为备选股票池
2. 利用机器学习方法，使用量价指标从股票池中挖掘短期强势的股票作为持仓股票
"""

import os
import pandas as pd
import numpy as np

from . select_stocls_multifactors import mfs_by_score
from Factor.config.path import PROJECT_FILES_PATH
from Factor.read import (
    get_secs_index_std,
    get_secs_multiple_index_stds,
    get_secs_index,
)
import devkit.api as dk
import finkit.api as fk
import ModelAPI.api as model


def mfs_by_LR(date, windows_step1, windows_step2, num1, num2, cycle, features, good_criterion=0.5):
    """
    基于逻辑回归从备选股票中选择强势股票 作为持仓股 返回股票列表
    @date <"%Y-%m-%d">: 开始建仓日期
    @windows_step1 <int>: 计算因子权重的滚动窗口 即根据近多少个交易日进行分组有效性检验
    @windows_step2 <int>: 建立ML模型时时间窗口
    @num1 <int>: 股票池数量
    @num2 <int>: 持仓股票数
    @cycle <int>: 持仓周期 持仓30天 就应该选择未来30天的年化收益率作为target
    @good_criterion <float>: 强势股票的定义 如=0.6 则大于60%分位数的股票为强势股 默认为0.5 为了防止不平衡问题
    @return 选择的股票 
    """
    stocks_pool = mfs_by_score(date, windows_step1, num1)
    datelist = fk.get_trading_days(end=date)
    datelist = sorted(datelist)
    datelist = datelist[-1 * windows_step2:]  # 获取date日期滞后周期个交易日的日期列表
    df_features = get_secs_multiple_index_stds(features, stocks_pool, datelist)
    close = get_secs_index('close', stocks_pool, datelist)
    close = close.sort_values(['sec_id', 'date']).reset_index()
    del close['index']
    close1 = close.copy()
    for sec_id in set(close.sec_id.tolist()):
        temp = close[close.sec_id == sec_id]
        for idx in temp.index[:-cycle]:
            date_now = dk.char2datetime(temp.loc[idx, 'date'])
            date_future = dk.char2datetime(temp.loc[idx + cycle, 'date'])
            timedelta = (date_future - date_now).days
            close1.loc[idx, 'time_delta'] = timedelta
            close1.loc[idx, 'close_future'] = temp.loc[idx + cycle, 'close']
            close1.loc[idx, 'future_ret'] = (temp.loc[idx + cycle, 'close'] / temp.loc[idx, 'close'] - 1) / timedelta * 365
    close2 = close1[close1.time_delta <= close1.time_delta.mode()[0]]  # 删除异常股票 间隔时间太长可能由于停牌
    train = df_features.merge(close2[['date', 'sec_id', 'future_ret']], how='inner', on=['date', 'sec_id'])
    train = dk.winsorize(train, 'future_ret', 0.01, 0.99)["normal_sector"]
    mid = train.future_ret.quantile(good_criterion)
    for i in train.index:
        if train.loc[i, 'future_ret'] > mid:
            train.loc[i, 'good_stock'] = 1
        else:
            train.loc[i, 'good_stock'] = 0
    del train['date']
    del train['future_ret']
    del train['sec_id']
    X = train.iloc[:, :-1]
    y = train.iloc[:, -1]
    lr = model.fit_LR(features=X, target=y)
    features_now = get_secs_multiple_index_stds(features, [], [date])
    del features_now['date']
    features_now = features_now.set_index('sec_id')
    prob = lr.predict_proba(features_now)
    prob_good = prob[:, lr.classes_.tolist().index(1)]
    features_now['prob_good'] = prob_good
    features_now_sort = features_now.sort_values(['prob_good'])
    selected_stocks = features_now_sort.iloc[-1 * num2:, :].index.tolist()
    return selected_stocks


def mfs_by_SVC(date, windows_step1, windows_step2, num1, num2, cycle, params, features, good_criterion=0.5):
    """
    基于SVC从备选股票中选择强势股票 作为持仓股 返回股票列表
    @date <"%Y-%m-%d">: 开始建仓日期
    @windows_step1 <int>: 计算因子权重的滚动窗口 即根据近多少个交易日进行分组有效性检验
    @windows_step2 <int>: 建立ML模型时时间窗口
    @num1 <int>: 股票池数量
    @num2 <int>: 持仓股票数
    @params <dict>: SVC的参数
    @cycle <int>: 持仓周期 持仓30天 就应该选择未来30天的年化收益率作为target
    @good_criterion <float>: 强势股票的定义 如=0.6 则大于60%分位数的股票为强势股 默认为0.5 为了防止不平衡问题
    @return 选择的股票 
    """
    stocks_pool = mfs_by_score(date, windows_step1, num1)
    datelist = fk.get_trading_days(end=date)
    datelist = sorted(datelist)
    datelist = datelist[-1 * windows_step2:]  # 获取date日期滞后周期个交易日的日期列表
    df_features = get_secs_multiple_index_stds(features, stocks_pool, datelist)
    close = get_secs_index('close', stocks_pool, datelist)
    close = close.sort_values(['sec_id', 'date']).reset_index()
    del close['index']
    close1 = close.copy()
    for sec_id in set(close.sec_id.tolist()):
        temp = close[close.sec_id == sec_id]
        for idx in temp.index[:-cycle]:
            date_now = dk.char2datetime(temp.loc[idx, 'date'])
            date_future = dk.char2datetime(temp.loc[idx + cycle, 'date'])
            timedelta = (date_future - date_now).days
            close1.loc[idx, 'time_delta'] = timedelta
            close1.loc[idx, 'close_future'] = temp.loc[idx + cycle, 'close']
            close1.loc[idx, 'future_ret'] = (temp.loc[idx + cycle, 'close'] / temp.loc[idx, 'close'] - 1) / timedelta * 365
    close2 = close1[close1.time_delta <= close1.time_delta.mode()[0]]  # 删除异常股票 间隔时间太长可能由于停牌
    train = df_features.merge(close2[['date', 'sec_id', 'future_ret']], how='inner', on=['date', 'sec_id'])
    train = dk.winsorize(train, 'future_ret', 0.01, 0.99)["normal_sector"]
    mid = train.future_ret.quantile(good_criterion)
    for i in train.index:
        if train.loc[i, 'future_ret'] > mid:
            train.loc[i, 'good_stock'] = 1
        else:
            train.loc[i, 'good_stock'] = 0
    del train['date']
    del train['future_ret']
    del train['sec_id']
    X = train.iloc[:, :-1]
    y = train.iloc[:, -1]
    svc = model.fit_SVC(features=X, target=y, params=params)
    features_now = get_secs_multiple_index_stds(features, [], [date])
    del features_now['date']
    features_now = features_now.set_index('sec_id')
    prob = svc.predict_proba(features_now)
    prob_good = prob[:, svc.classes_.tolist().index(1)]
    features_now['prob_good'] = prob_good
    features_now_sort = features_now.sort_values(['prob_good'])
    selected_stocks = features_now_sort.iloc[-1 * num2:, :].index.tolist()
    return selected_stocks
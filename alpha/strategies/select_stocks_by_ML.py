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


def mfs_by_LR(date, windows_step1, windows_step2, num1, num2, cycle, features):
    """
    基于逻辑回归从备选股票中选择强势股票 作为持仓股 返回股票列表
    @date <"%Y-%m-%d">: 开始建仓日期
    @windows_step1 <int>: 计算因子权重的滚动窗口 即根据近多少个交易日进行分组有效性检验
    @windows_step2 <int>: 建立ML模型时时间窗口
    @num1 <int>: 股票池数量
    @num2 <int>: 持仓股票数
    @cycle <int>: 持仓周期 持仓30天 就应该选择未来30天的年化收益率作为target
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
    train1 = df_features.merge(close2[['date', 'sec_id', 'future_ret']], how='inner', on=['date', 'sec_id'])
    qua = train1['future_ret'].quantile(0.75)
    train1['goodyn'] = train1['future_ret'].apply(lambda x: 1 if x > qua else 0)
    
    return train1
    index_info = dk.json2dict(os.path.join(PROJECT_FILES_PATH, "factor_weight", "cycle{}".format(str(windows)), "{}.json".format(date)))
    index_std_all = pd.DataFrame()
    weight = {key: index_info[key]['weight'] for key in index_info}  # 有效因子权重
    monotony = {key: index_info[key]['ascending'] for key in index_info}  # 因子单调方向
    for index_std in weight:
        if len(index_std_all) == 0:
            index_std_all = get_secs_index_std(index_std, trading_days=[date])[['sec_id', index_std]]
        else:
            temp = get_secs_index_std(index_std, trading_days=[date])[['sec_id', index_std]]
            index_std_all = index_std_all.merge(temp, how='inner', on=['sec_id'])
    index_std_all = index_std_all.set_index(['sec_id'])
    # 获取每个因子的单调方向 目的是使最优因子排名靠前
    ascending = [key for key in monotony if monotony[key] == 1.0]  # 反向因子  越小越好
    descending = [key for key in monotony if monotony[key] == 0.0]  # 正向因子 越大越好
    part1 = index_std_all[descending].rank(ascending=False)  # 对正向因子进行排序
    part2 = index_std_all[ascending].rank(ascending=True)  # 对反向因子进行排序
    index_std_all1 = part1.merge(part2, how='inner', left_index=True, right_index=True)
    index_std_all2 = index_std_all1.copy()
    # 获取不同因子的加权排名
    for col in index_std_all1.columns:
        index_std_all2[col] = index_std_all2[col] * weight[col]
    selected_stocks = index_std_all2.sum(axis=1).sort_values().index[:num].tolist()  # 选出排名前20的股票
    return selected_stocks

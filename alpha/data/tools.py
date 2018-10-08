# -*- coding: utf-8 -*-
"""
一些工具函数
"""

import pandas as pd
import numpy as np


# 方案1 label_A 分位数法  次月收率处于同期前30%的为1（强势股） 位于后30%的为0（弱势股）
def derive_label_A(dsi, lp=0.3, up=0.7):
    """
    根据给定的数据集dsi计算标签
    @up <int>: 上限 大于此值为强势股 记为1
    @lp <int>: 下限 小于于此值为弱势股 记为0
    """
    df_lp = dsi.groupby(['yearmonth']).month_ret.apply(lambda x: x.quantile(lp)).reset_index().rename(columns={'month_ret': 'lp'})
    df_up = dsi.groupby(['yearmonth']).month_ret.apply(lambda x: x.quantile(up)).reset_index().rename(columns={'month_ret': 'up'})
    dsi = dsi.merge(df_lp, how='left', on='yearmonth')
    dsi = dsi.merge(df_up, how='left', on='yearmonth')
    for i in dsi.index:
        if dsi.loc[i, 'month_ret'] < dsi.loc[i, 'lp']:
            dsi.loc[i, 'good_yn'] = 0
        elif dsi.loc[i, 'month_ret'] > dsi.loc[i, 'up']:
            dsi.loc[i, 'good_yn'] = 1
        else:
            dsi.loc[i, 'good_yn'] = np.nan
    del dsi['lp']
    del dsi['up']
    dsi = dsi[~dsi.good_yn.isnull()]
    return dsi

# 方案2 label_B 绝对收益法    次月收益率>0 为1 否则为0


def derive_label_B(dsi):
    """
    根据给定的数据集dsi计算标签
    """
    dsi['good_yn'] = (dsi['month_ret'] > 0) * 1

    del dsi['month_ret']
    dsi = dsi[~dsi.good_yn.isnull()]
    return dsi

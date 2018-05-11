# -*- coding: utf-8 -*-

"""
factor.py

从本地数据库载入原始indicators 然后计算因子

@author: Gui lichao
@email:
@date: 2017.12.28

-------------------

计算方法：
- 读取factor数据时取出极端值，阈值同winsorize 一致

FUNCTION LIST:
- load_single_factor_return_on_multidays(factor, trading_days, group_num=10)
"""

import os
import numpy as np
import pandas as pd

from devkit.api import json2dict, Logger
from .. config.path import DB_PATH
from .. read.factor import get_secs_factor
from .. factor.const import WINSORIZE_LB, WINSORIZE_UB
from .. read.indicator import get_adjusted_close_price


def load_single_factor_return_on_multidays(factor, trading_days, group_num=10):
    """
    加载单个日期单个factor的return信息

    @factor (str):  指标名称
    @trading_days (['%Y-%m-%d']): 日期列表
    @group_num (int): 分组个数 默认为10
    return: DataFrame，列名:date group01-group-10 factor_return
    """

    output = pd.DataFrame()
    close_pre = get_adjusted_close_price(date=trading_days[0])

    for i, date in enumerate(trading_days[1:]):
        date_pre = trading_days[i]
        close_curr = get_adjusted_close_price(date=date)
        df_return = (close_curr / close_pre - 1.).rename(columns={"CLOSE": "RETURN"})

        factor_pre = get_secs_factor(factor=factor, date=date_pre, log=False).reset_index()
        lower, upper = factor_pre[factor].quantile([WINSORIZE_LB, WINSORIZE_UB])
        selected_list = np.array(lower < factor_pre[factor]) & np.array(factor_pre[factor] < upper)
        factor_pre = factor_pre[selected_list]
        df_all = df_return.merge(factor_pre, how="inner", left_index=True, right_on='sec_id')
        df_all = df_all[df_all[factor] != 0.0].copy()   # 删除缺失数据
        # 分组并计算各组收益
        df_all = df_all.sort_values(by=factor)
        df_all["group"] = np.nan  # 表示缺失
        n_sample = df_all.shape[0]
        dist = int(n_sample / group_num)  # 每组个数
        col_index = df_all.columns.tolist().index("group")
        for j in range(group_num):
            if j < group_num - 1:
                df_all.iloc[j * dist:(j + 1) * dist, col_index] = j
            else:
                df_all.iloc[j * dist:, col_index] = j
        df_group = df_all[['RETURN', 'group']].groupby(by='group').mean()

        # 转置，使每组成为一个变量
        df_final = df_group.transpose()
        new_names = ['group{:0>2}'.format(i) for i in range(1, group_num + 1)]
        df_final.columns = new_names  # 重新命名

        # 计算变量factor的值: factor = 最后一组和第一组return的差
        if factor == 'SIZE':  # 对于SIZE因子，第一组中包含很多新股，不具代表性，所以用最后一组减去第二组
            df_final['SIZE'] = df_final[new_names[-1]] - df_final[new_names[1]]
        else:
            df_final["{}".format(factor)] = df_final[new_names[-1]] - df_final[new_names[0]]

        # 加入变量date
        df_final["date"] = date
        df_final = df_final.reset_index(drop=True)
        # print(df_final)
        output = output.append(df_final)

        # 将当前价赋给过去 以便在计算下一个日期时无需重新计算上期收盘价
        close_pre = close_curr.copy()
    return output

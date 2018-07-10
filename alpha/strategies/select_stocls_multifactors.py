# -*- coding: utf-8 -*-

"""
select_stocls_multifactors.py
多因子选股模型

"""
import os
import devkit.api as dk
import pandas as pd
import numpy as np
from sklearn.decomposition import KernelPCA
from sklearn.svm import SVR
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
from sklearn.preprocessing import scale
from sklearn.model_selection import train_test_split
from Factor.config.path import PROJECT_FILES_PATH
from Factor.read import get_secs_index_std


def mfs_by_score(date, windows_step1, num1):
    """
    打分法多因子选股: 给定指定日期，计算当天因子打分情况 返回选定股票
    @date <"%Y-%m-%d">: 开始建仓日期
    @windows_step1 <int>: 计算因子权重的滚动窗口 即根据近多少个交易日进行分组有效性检验
    @num1 <int>: 持仓股票数
    @return 选择的股票 
    """

    index_info = dk.json2dict(os.path.join(PROJECT_FILES_PATH, "factor_weight", "cycle{}".format(str(windows_step1)), "{}.json".format(date)))
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
    selected_stocks = index_std_all2.sum(axis=1).sort_values().index[:num1].tolist()  # 选出排名前20的股票
    return selected_stocks

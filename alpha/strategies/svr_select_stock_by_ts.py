# -*- coding: utf-8 -*-

"""
基于SVR模型 以年报中的财务指标为features，股票的年收益率为label 建立SVR模型
target variable: 年收益率
features：
选股范围：
训练期：
测试集：
模型：
参数：


comments
1. 简化起见申万行业分类采取的是最新申万行业，然后匹配到过去，因此并没有考虑某个上市公司的行业变化

"""
import devkit.api as dk
import pandas as pd
import numpy as np
from sklearn.decomposition import KernelPCA
from sklearn.svm import SVR
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
from sklearn.preprocessing import scale
from sklearn.model_selection import train_test_split


ts_szzz11 = pd.read_csv(r"E:\99_daily\TODAY\szzz.csv")  # 上证综指2000-2018年前复权收盘价及其他ts指标

# 设置自变量和因变量
ts_szzz1['x1'] = np.nan
ts_szzz1['x2'] = np.nan
ts_szzz1['x3'] = np.nan
ts_szzz1['y'] = np.nan

id_x1 = ts_szzz1.columns.tolist().index('x1')
id_x2 = ts_szzz1.columns.tolist().index('x2')
id_x3 = ts_szzz1.columns.tolist().index('x3')
id_y = ts_szzz1.columns.tolist().index('y')
id_close = ts_szzz1.columns.tolist().index('close')

for i in range(close.shape[0]):
    if i > 2 and i < close.shape[0] - 1:
        ts_szzz1.iloc[i, id_x1] = ((ts_szzz1.iloc[i, id_close] / ts_szzz1.iloc[i - 1, id_close]) - 1) * 100
        ts_szzz1.iloc[i, id_x2] = ((ts_szzz1.iloc[i, id_close] / ts_szzz1.iloc[i - 2, id_close]) - 1) * 100
        ts_szzz1.iloc[i, id_x3] = ts_szzz1.iloc[i, id_close] - (ts_szzz1.iloc[i - 1, id_close] + ts_szzz1.iloc[i - 2, id_close] + ts_szzz1.iloc[i - 3, id_close]) / 3
        ts_szzz1.iloc[i, id_y] = 100 * (ts_szzz1.iloc[i + 1, id_close] / (ts_szzz1.iloc[i - 1, id_close] + ts_szzz1.iloc[i - 2, id_close] + ts_szzz1.iloc[i, id_close]) * 3 - 1)

ts_szzz2 = ts_szzz1.set_index('date')


train_pre1 = ts_szzz2[['x1', 'x2', 'x3', 'y']]
train_pre2 = train_pre1.dropna()
train_pre1 = ts_szzz2[['x1', 'x2', 'x3', 'y']]
train_pre2 = train_pre1.dropna()
train_pre3 = train_pre2.apply(lambda x: (x - x.mean()) / x.std())  # 统计标准化


def handle_outliers(x):
    x[np.abs(x) > 3] = 3
    return x

train_pre4 = train_pre3.apply(lambda x: handle_outliers(x))  # 盖帽法处理极端值

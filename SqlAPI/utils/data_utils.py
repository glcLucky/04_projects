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

import pandas as pd

from devkit.api import Logger


def mark_missing(data, var):
    """
    分离缺失值和非缺失值，并将缺失值赋为0.0
    :param: data (DataFrame): 第一列为sec_id 第二列为value
    :return: tuple（non-missing,missing）
    """

    df_non_missing = data[data[var].notnull()].copy()
    df_missing = data[data[var].isnull()].copy().fillna(0.)
    return {
        "non_missing": df_non_missing,
        "missing": df_missing,
    }


def winsorize(data, var, lower_quanile, upper_quantile):
    """
    对给定数据进行winsorize
    :param: data (DataFrame): 待winsorize数据框
    :param: var (str): 待winsorize的变量
    :param: lower_quanile（float, 0-1): 下限
    :param: upper_quantile（float, 0-1): 上限
    :return: winsorize后的data（dict）:
             key: lower_sector normal_sector upper_sector
             value: 对应的DataFrame
    """

    assert 0 <= lower_quanile < upper_quantile <= 1

    data_sorted = data.sort_values(by=var).copy()
    length = len(data)
    lower_index = int(lower_quanile * length) + 1
    upper_index = int(upper_quantile * length)
    lower_sector = data_sorted.iloc[:lower_index, :].copy()
    normal_sector = data_sorted.iloc[lower_index:upper_index, :].copy()
    upper_sector = data_sorted.iloc[upper_index:, :].copy()

    return {
        "lower_sector": lower_sector,
        "normal_sector": normal_sector,
        "upper_sector": upper_sector
    }


def standardize(data):
    """
    对给定数据进行统计标准化
    :param: data (Series)
    :return: 标准化后的Series
    """

    mean = data.mean()
    std = data.std()
    output = data.copy()
    output = (output - mean) / std
    return output


def statistical_process(data, var, winsor_LB, winsor_UB):
    """
    对数据进行预处理，包括缺失值分离，去极值，和统计标准化

    @data (DataFrame): 待处理数据
    @var (str): 待处理变量名
    return (DdataFrame) 预处理完成的数据框
    """

    # 缺失值分离
    result = mark_missing(data=data, var=var)
    factor_non_missing = result['non_missing']
    factor_missing = result['missing']

    # winsorize
    result = winsorize(
        data=factor_non_missing,
        var=var,
        lower_quanile=winsor_LB,
        upper_quantile=winsor_UB,
    )

    lower_sector = result['lower_sector']
    normal_sector = result['normal_sector']
    upper_sector = result['upper_sector']

    # 统计标准化
    normal_sector[var] = standardize(normal_sector[var])
    lower_sector[var] = normal_sector[var].min()
    upper_sector[var] = normal_sector[var].max()

    # 合并数据集
    factor_final = normal_sector
    for supplements in (factor_missing, lower_sector, upper_sector):
        factor_final = factor_final.append(supplements)

    factor_final = factor_final.sort_values(by=['sec_id'])

    return factor_final

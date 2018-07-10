# -*- coding: utf-8 -*-

"""
preprocessing.py

数据预处理函数

@author: Gui jasper
@email: 
@date: 2018.05.12

---------------

FUNCTION LIST:
- df_sampling(df, nsamples, force=True)
"""


def winsorize(data, var, lower_quanile, upper_quantile):
    """
    对给定数据进行按照指定分位数winsorize
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
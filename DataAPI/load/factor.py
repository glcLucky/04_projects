# -*- coding: utf-8 -*-

"""
factor.py

从本地数据库载入原始indicators 然后计算因子

@author: Jasper Gui
@email: jasper.gui@outlook.com
@date: 2018.03.08

-------------------

FUNCTION LIST:
- load_single_factor_on_single_day(factor, date)
"""

import os

from devkit.api import Logger

from .. factor import calculate_factor


def load_single_factor_on_single_day(factor, date):
    """
    加载单个日期单个factor的信息

    @factor (str): 因子名称
    @date ("%Y-%m-%d"): 单个日期
    :return: DataFrame, columns=['sec_id', <factor_name>]
    """

    return calculate_factor(factor, date)

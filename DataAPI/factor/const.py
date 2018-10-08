# -*- coding: utf-8 -*-

"""
const.py

配置计算因子所需的全局变量

@author: Jasper Gui
@email: jasper.gui@outlook.com
@date: 2018.03.08
"""

# winsorize 的参数，极值的分位定义
WINSORIZE_LB = 0.01
WINSORIZE_UB = 0.99

# 缺失阈值，缺失值超过30%的数据认为无效
MISSING_CRITERION = 0.3

# -*- coding: utf-8 -*-

"""
utils.py

工具函数

@author: Wu Yudi
@email: wuyd@swsresearch.com
@date: 2017.01.10
"""

# import pandas as pd


def options2str(options):
    return ";".join("{}={}".format(key, val) for key, val in options.items() if val is not None)


def test_error(response):
    if response.ErrorCode:
        raise ValueError(response.Data[0][0])


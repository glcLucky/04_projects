# -*- coding: utf-8 -*-

"""
wind_industry_apis.py

根据自己的需求创建的特殊API

@author: Wu Yudi
@email: wuyd@swsresearch.com
@date: 2017.01.10


function list:
- get_secs_industry
- get_secs_industry_sw
- get_secs_industry_gics
"""
import pandas as pd

import WindAPI
from finkit.api import classify_equity
from WindPy import w as WDServer

from . resources import (
    SWL1_CODE2NAME,
    SWL2_CODE2NAME,
    SWL3_CODE2NAME,

    GICS1_CODE2NAME,
    GICS2_CODE2NAME,
    GICS3_CODE2NAME,
)

from . utils import options2str, test_error

SW_FIELDS_MAP = {
    "A": ["windcode", "industry_swcode", "industry_sw"],
    "H": ["windcode", "industry_swcode_hk", "industry_sw_hk"]
}


def get_secs_industry(sec_ids=[], date="", level=1):
    """
    获取股票行业分类，A股为申万行业分类（按level来），港股为GICS行业分类

    @parameters:
    sec_ids (list of str): 证券代码列表
    date (str): 查询日期
    level (int): 行业层级，1、2、3分别对应申万一级、二级、三级分类

    return (dict of str): 键是证券代码，值是行业名称
    """

    classified_secs = classify_equity(sec_ids)
    if classified_secs["其他"]:
        print("Unvalid security IDs:")
        print(classified_secs["其他"])
        raise ValueError

    ind = get_secs_industry_sw(classified_secs["A股"], date, level, "A")
    ind_gics = get_secs_industry_gics(classified_secs["港股"], level)

    ind.update(ind_gics)
    return ind


def get_secs_industry_sw(sec_ids=[], date="", level=1, market="A"):
    """
    获取股票列表申万行业分类

    @parameters:
    sec_ids (list of str): 证券代码列表
    date (str): 查询日期
    level (int): 行业层级，1、2、3分别对应申万一级、二级、三级分类
    market (str): 证券市场 A:表示A股市场 H:表示港股市场

    return (dict of str): 键是证券代码，值是行业名称
    """

    WindAPI.login(is_quiet=True)

    date = date.replace("-", "")

    if not sec_ids:
        return {}

    levelmap = {1: SWL1_CODE2NAME, 2: SWL2_CODE2NAME, 3: SWL3_CODE2NAME}
    lookup = levelmap[level]

    fields = SW_FIELDS_MAP[market]
    options = {"tradDate": date.replace("-", ""),
               "industryType": level}

    response = WDServer.wss(codes=",".join(sec_ids),
                            fields=",".join(fields),
                            options=options2str(options))
    test_error(response)

    output = {}
    for i, sec in enumerate(response.Data[0]):
        if response.Data[1][i] in lookup:
            output[sec] = lookup[response.Data[1][i]]
        elif response.Data[2][i]:
            output[sec] = response.Data[2][i]
    return output


def get_secs_industry_gics(sec_ids=[], level=1):
    """
    获取股票列表GICS行业分类

    @parameters:
    sec_ids (list of str): 证券代码列表，4位，后缀.HK
    return (dict of str): 键是证券代码，值是行业名称
    """

    if not sec_ids:
        return {}

    WindAPI.login(is_quiet=True)

    levelmap = {1: GICS1_CODE2NAME, 2: GICS2_CODE2NAME, 3: GICS3_CODE2NAME}
    lookup = levelmap[level]

    fields = ["windcode", "industry_gicscode", "industry_gics"]
    options = {"industryType": level}

    response = WDServer.wss(codes=",".join(sec_ids),
                            fields=",".join(fields),
                            options=options2str(options))
    test_error(response)

    output = {}
    for i, sec in enumerate(response.Data[0]):
        if response.Data[1][i] in lookup:
            output[sec] = lookup[response.Data[1][i]]
        elif response.Data[2][i]:
            output[sec] = response.Data[2][i]

    return output

# -*- coding: utf-8 -*-

"""
industry.py

行业相关的API

@author: Jasper Gui
@email: jasper.gui@outlook.com
@date: 2017.12.11

-------------------

FUNCTION LIST:
- load_secs_industry_sw_from_wind(index_code, date, level=1)
- load_secs_industry_gics_from_wind(index_code, date, level=1)
"""

import os

from devkit.api import Logger
from WindAPI.wind_industry_apis import get_secs_industry_sw, get_secs_industry_gics

from .. read import get_index_contents


def load_secs_industry_sw_from_wind(index_code, date, level=1):
    """
    从Wind更新指定index成分股的申万行业数据

    @index_code (str): 指数代码 可选代码: "A" "H"
    @date (%Y-%m-%d): 单个日期
    @level (int): 行业级数 默认为1 表示为申万1级行业分类
    :return: (dict of str): 键是证券代码，值是行业名称
    """

    universe = get_index_contents(index_code, date, log=False)

    if not universe:
        Logger.error("Empty universe at {}!".format(date))
        return {}

    output = get_secs_industry_sw(sec_ids=universe, date=date, level=level, market=index_code)
    return output


def load_secs_industry_gics_from_wind(index_code, date, level=1):
    """
    从Wind更新指定index成分股的gics行业数据

    @index_code (str):  "H_GICSL1"
    @date (%Y-%m-%d):  单个日期
    @level (int): 行业级数 默认为1 表示为申万1级行业分类
    :return: (dict of str): 键是证券代码，值是行业名称
    """

    universe = get_index_contents(index_code, date)

    if not universe:
        Logger.error("Empty universe at {}!".format(date))
        return {}

    output = get_secs_industry_gics(sec_ids=universe, level=1)
    return output

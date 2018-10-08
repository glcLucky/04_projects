# -*- coding: utf-8 -*-

"""
industry.py

读取行业信息的API

@author: Jasper Gui
@email: jasper.gui@outlook.com
@date: 2018.03.08

-------------------

FUNCTION LIST:
- get_secs_industry(industry_code, sec_ids=[], date="")
- get_secs_industry_SWL1(sec_ids=[], date="")
- get_secs_industry_from_sql(industry_code, sec_ids=[], date="")
- get_secs_industry_from_json(industry_code, sec_ids=[])
"""

import os

from devkit.api import (
    Logger,
    json2dict,
    SqliteProxy
)
from finkit.api import classify_equity

from .. config.path import DB_PATH_LIB

DB_INDUSTRY = DB_PATH_LIB['industry']
INDUSTRY_AS_SQL = ("A_SWL1", )
INDUSTRY_AS_JSON = ("H_GICSL1", "H_SWL1")


def get_secs_industry(industry_code, sec_ids=[], date=""):
    """
    获取某日期某些股票的的行业分类信息，数据格式 {股票代码：行业分类}

    @industry_code (str): 子数据库名称，目前支持 ["A_SWL1", "H_SWL1", "H_GICSL1"]
    @sec_ids: (list) 股票列表
    @date: ("%Y-%m-%d") 单个日期
    return: {sec_id: industry}，不存在则忽略
    """

    if len(sec_ids) == 0:
        Logger.warn("Empty sec_ids when reading {} on {}!".format(industry_code, date))
        return {}

    if industry_code in INDUSTRY_AS_SQL:
        output = get_secs_industry_from_sql(industry_code, sec_ids, date)
    elif industry_code in INDUSTRY_AS_JSON:
        output = get_secs_industry_from_json(industry_code, sec_ids)
    else:
        Logger.error("Unrecognized industry code: {}".format(industry_code))
        raise ValueError
    return output


def get_secs_industry_SWL1(sec_ids=[], date=""):
    """
    获取某日期某些股票的的申万一级行业分类信息，自动处理A股和H股，数据格式 {股票代码：行业分类}

    @sec_id: (list) 股票列表
    @date: (%Y-%m-%d) 单个日期
    """

    if len(sec_ids) == 0:
        Logger.warn("Empty sec_ids when reading SWL1 on {}!".format(date))
        return {}

    classfier = classify_equity(sec_ids)

    output_A = {}
    if classfier['A股']:
        output_A = get_secs_industry(industry_code="A_SWL1", sec_ids=classfier['A股'], date=date)

    output_H = {}
    if classfier['港股']:
        output_H = get_secs_industry(industry_code="H_SWL1", sec_ids=classfier['港股'], date=date)

    output_A.update(output_H)
    return output_A


def get_secs_industry_from_sql(industry_code, sec_ids=[], date=""):
    dbpath = os.path.join(DB_INDUSTRY, '{}.db'.format(date[:4]))
    with SqliteProxy(log=False) as proxy:
        proxy.connect(dbpath)
        if len(sec_ids) == 1:
            query = "SELECT sec_id, industry FROM [{}] WHERE date='{}' and sec_id = '{}'".format(industry_code, date, sec_ids[0])
        else:
            query = "SELECT sec_id, industry FROM [{}] WHERE date='{}' and sec_id in {}".format(industry_code, date, tuple(sec_ids))
        df = proxy.query_as_dataframe(query).set_index('sec_id')
        return {sec_id: df.at[sec_id, 'industry'] for sec_id in sec_ids if sec_id in df.index}


def get_secs_industry_from_json(industry_code, sec_ids=[]):
    path = os.path.join(DB_INDUSTRY, '{}.json'.format(industry_code))
    info = json2dict(path, validate=True)
    return {sec: info[sec] for sec in sec_ids if sec in info}

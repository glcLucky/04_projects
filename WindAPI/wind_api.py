# -*- coding: utf-8 -*-

"""
wind_api.py

根据自己的需求创建的特殊API

@author: Wu Yudi
@email: wuyd@swsresearch.com
@date: 2017.01.10
"""

import pandas as pd
from WindPy import w as WDServer
from finkit.api import get_nearest_trading_day

from . resources import (
    SWL1_CODE2NAME,
    SWL2_CODE2NAME,
    SWL3_CODE2NAME,
)
from . utils import options2str, test_error


def get_trading_days(start_date, end_date):
    response = WDServer.tdays(beginTime=start_date, endTime=end_date)
    test_error(response)
    return [dt.strftime("%Y-%m-%d") for dt in response.Data[0]]


def get_sector_contents(date, sector_code="a001010100000000"):
    # 全A股：a001010100000000

    options = {"date": date,
               "sectorid": sector_code}
    response = WDServer.wset(tablename="sectorconstituent", options=options2str(options))
    test_error(response)
    output = {"股票代码": response.Data[1],
              "股票名称": response.Data[2]}
    return pd.DataFrame(output)


def get_index_contents(date, index_code="000300.SH"):
    options = {"date": date,
               "windcode": index_code}
    response = WDServer.wset(tablename="indexconstituent", options=options2str(options))
    test_error(response)
    output = {"股票代码": response.Data[1],
              "股票名称": response.Data[2],
              "股票权重": [x/100 if x is not None else 0. for x in response.Data[3]]}
    return pd.DataFrame(output)


def get_secs_name(sec_ids=[]):
    """
    获取日线数据

    @parameters:
    sec_ids (list of str): 证券代码列表
    date (str): 查询日期
    level (int): 行业层级，1、2、3分别对应申万一级、二级、三级分类

    return (dict of str): 键是证券代码，值是行业名称
    """

    if not sec_ids:
        return {}

    fields = ["windcode", "sec_name"]
    response = WDServer.wss(codes=",".join(sec_ids),
                            fields=",".join(fields))
    test_error(response)
    output = dict(zip(*response.Data))
    return output


def get_secs_liqshare(sec_ids=[], date=""):
    """
    获取流通股本

    @parameters:
    sec_ids (list of str): 证券代码列表
    date (str): 查询日期

    return (dict of dict): 键是证券代码，值是总流动股本
    """

    fields = ["windcode", "float_a_shares"]
    options = {"tradDate": date,
               "unit": "1"}
    response = WDServer.wss(codes=",".join(sec_ids),
                            fields=",".join(fields),
                            options=options2str(options))
    test_error(response)
    output = dict(zip(*response.Data))
    return output


def get_secs_market_cap(sec_ids=[], date=""):
    """
    获取流通市值

    @parameters:
    sec_ids (list of str): 证券代码列表
    date (str): 查询日期

    return (dict of dict): 键是证券代码，值是流通市值
    """

    if not sec_ids:
        return {}

    date = date.replace("-", "")

    fields = ["windcode", "mkt_cap_float"]
    options = {"tradDate": date,
               "unit": "1",
               "currencyType": ""}
    response = WDServer.wss(codes=",".join(sec_ids),
                            fields=",".join(fields),
                            options=options2str(options))
    test_error(response)
    output = dict(zip(*response.Data))
    return output

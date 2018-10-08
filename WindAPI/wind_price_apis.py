# -*- coding: utf-8 -*-

"""
wind_price_apis.py

根据自己的需求创建的特殊API

@author: Jasper Gui
@email: wuyd@swsresearch.com
@date: 2017.01.10


function list:
- get_daily_prices
- get_single_attribute
- get_daily_single_attribute
- get_single_day_prices
"""

import pandas as pd
from WindPy import w as WDServer

from . utils import options2str, test_error


def get_single_attribute(sec_ids=[], start_date="", end_date="",
                         attribute='close', freq="D", adjust=None, **kwargs):
    """
    获取不同频率的单指标数据

    @parameters:
    sec_ids (list of str): 证券代码列表
    start_date (str): 起始时间（包含）
    end_data (str): 结束时间（包含）
    field (list of str): 查询字段，可用open, high, low, close, pre_close, volume, amt(成交额), trade_status(交易状态)
    freq (str): 数据频率，D为日，W为周，M为月，Y为年
    adjust (str): 复权方式，None为不复权，B为后复权，F为前复权

    return (dict of DataFrame): 键是证券代码，值是DataFrame，行为日期，列为field
    """

    start_date = start_date.replace("-", "")
    end_date = end_date.replace("-", "")

    options = kwargs
    options["Period"] = freq
    options["PriceAdj"] = adjust
    options["Fill"] = "Previous"
    response = WDServer.wsd(codes=",".join(sec_ids),
                            fields=attribute,
                            beginTime=start_date,
                            endTime=end_date,
                            options=options2str(options))
    test_error(response)
    trading_days = [dt.strftime("%Y-%m-%d") for dt in response.Times]
    if len(response.Codes) == 1:
        df = {response.Codes[0]: response.Data[0]}
    elif len(response.Times) == 1:
        df = {sec: response.Data[0][i] for i, sec in enumerate(response.Codes)}
    else:
        df = {sec: response.Data[i] for i, sec in enumerate(response.Codes)}
    return pd.DataFrame(df, index=trading_days)


def get_daily_single_attribute(sec_ids=[], start_date="", end_date="",
                               attribute='close', adjust=None, **kwargs):
    """
    获取日线单指标数据

    @parameters:
    sec_ids (list of str): 证券代码列表
    start_date (str): 起始时间（包含）
    end_data (str): 结束时间（包含）
    field (list of str): 查询字段，可用open, high, low, close, pre_close, volume, amt(成交额), trade_status(交易状态)
    adjust (str): 复权方式，None为不复权，B为后复权，F为前复权

    return (dict of DataFrame): 键是证券代码，值是DataFrame，行为日期，列为field
    """

    return get_single_attribute(sec_ids=sec_ids,
                                start_date=start_date,
                                end_date=end_date,
                                attribute=attribute,
                                freq="D",
                                adjust=adjust)


def get_single_day_attributes(sec_ids=[], date="", fields=[], **kwargs):
    """
    获取单日指标数据

    @parameters:
    sec_ids (list of str): 证券代码列表
    start_date (str): 起始时间（包含）
    end_data (str): 结束时间（包含）
    fields (list of str): 查询字段
    adjust (str): 复权方式，None为不复权，B为后复权，F为前复权

    return (DataFrame): 行是证券代码，列为field
    """

    if not sec_ids:
        print("Empty sec_ids!")
        raise ValueError

    if not fields:
        print("Empty fields!")
        raise ValueError

    options = kwargs
    options["tradeDate"] = date.replace("-", "")
    response = WDServer.wss(codes=",".join(sec_ids),
                            fields=",".join(fields),
                            options=options2str(options))
    test_error(response)
    df = {field: response.Data[i] for i, field in enumerate(response.Fields)}
    df = pd.DataFrame(df, index=response.Codes)
    return df


def get_daily_prices(sec_ids=[], start_date="", end_date="",
                     fields=["open", "high", "low", "close", "volume", "amt"],
                     adjust=None, **kwargs):
    """
    获取日线数据

    @parameters:
    sec_ids (list of str): 证券代码列表
    start_date (str): 起始时间（包含）
    end_data (str): 结束时间（包含）
    fields (list of str): 查询字段，可用open, high, low, close, preclose, volume, amount(成交额), highlimit, lowlimit(是否涨跌停), tradestatus(状态)
    adjust (str): 复权方式，None为不复权，B为后复权，F为前复权

    return (dict of DataFrame): 键是证券代码，值是DataFrame，行为日期，列为field
    """

    start_date = start_date.replace("-", "")
    end_date = end_date.replace("-", "")

    options = kwargs
    options["PriceAdj"] = adjust
    options["Fill"] = "Previous"
    trading_days = None

    output = {}
    for sec in sec_ids:
        response = WDServer.wsd(codes=sec,
                                fields=",".join(fields),
                                beginTime=start_date,
                                endTime=end_date,
                                options=options2str(options))
        test_error(response)
        if trading_days is None:
            trading_days = [dt.strftime("%Y-%m-%d") for dt in response.Times]
        df = {field: response.Data[i]
              for i, field in enumerate(response.Fields)}
        output[sec] = pd.DataFrame(df, index=trading_days)
    return output
    


def get_single_day_prices(sec_ids=[], date="", fields=["open", "high", "low", "close", "volume", "amt"],
                          adjust=None, **kwargs):
    """
    获取单日行情数据

    @parameters:
    sec_ids (list of str): 证券代码列表
    date (str): 目标日期
    fields (list of str): 查询字段，可用open, high, low, close, preclose, volume, amount(成交额), highlimit, lowlimit(是否涨跌停), tradestatus(状态)
    adjust (str): 复权方式，None为不复权，B为后复权，F为前复权

    return (DataFrame): 行是证券代码，列为field
    """

    options = kwargs
    options["tradeDate"] = date
    options["PriceAdj"] = adjust
    options["Fill"] = "Previous"
    response = WDServer.wss(codes=",".join(sec_ids),
                            fields=",".join(fields),
                            options=options2str(options))
    test_error(response)
    df = {field: response.Data[i] for i, field in enumerate(response.Fields)}
    df = pd.DataFrame(df, index=response.Codes)
    return df

# -*- coding: utf-8 -*-

"""
index_content.py

下载指数成分股的API

@author: Wu Yudi
@email: jasper.wuyd@gmail.com
@date: 2017.12.19

-------------------

FUNCTION LIST:
- load_index_contents_from_wind(index_code, date)
- load_index_contents_and_weights_from_wind(index_code, date)
"""

import pandas as pd

import WindAPI
from WindAPI import WDServer, options2str

SECTOR_MAP = {
    "A": "a001010100000000",
    "H": "a002010100000000",
    "HSI.HI": "a003090101000000"
}


def load_index_contents_from_wind(index_code, date=""):
    """
    从wind下载某天某市场的全部股票数据或指数成分股数据

    @index_code (str): 指数代码
    @date ("%Y-%m-%d"): 单个日期，对于H、HSI.HI而言日期参数没用
    :return: DataFrame, columns=['sec_id', 'sec_name']
    """

    WindAPI.login(is_quiet=True)

    options = {
        "date": date,
        "sectorid": SECTOR_MAP[index_code]
    }
    response = WDServer.wset(tablename="sectorconstituent", options=options2str(options))
    WindAPI.test_error(response)
    output = {
        "sec_id": response.Data[1],
        "sec_name": response.Data[2]
    }
    return pd.DataFrame(output).loc[:, ["sec_id", "sec_name"]]


def load_index_contents_and_weights_from_wind(index_code, date):
    """
    从wind下载某天某指数成分股数据及权重

    @index_code (str): 指数编码 可选：000300.SH, 000016.SH, 000905.SH
    @date (%Y-%m-%d): 单个日期
    :return: DataFrame, columns=['sec_id', 'sec_name', 'weight']
    """

    WindAPI.login(is_quiet=True)

    options = {
        "date": date,
        "windcode": index_code
    }

    response = WDServer.wset(tablename="indexconstituent", options=options2str(options))
    WindAPI.test_error(response)
    output = {
        "sec_id": response.Data[1],
        "sec_name": response.Data[2],
        "weight": [x / 100. if x else 0. for x in response.Data[3]]
    }
    return pd.DataFrame(output).loc[:, ["sec_id", "sec_name", "weight"]]

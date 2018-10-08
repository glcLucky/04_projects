# -*- coding: utf-8 -*-

"""
indicator.py

下载指标原始数据

@author: Jasper Gui
@email: jasper.gui@outlook.com
@date: 2017.12.19

-------------------

FUNCTION LIST:
- load_single_indicator_on_single_day_from_wind(indicator, date)
"""

import pandas as pd

from devkit.api import Logger
import WindAPI
from WindAPI import WDServer, options2str

from .. schema import get_schema
from .. read.index_contents import get_index_contents

SCHEMA = get_schema("indicator")


def load_single_indicator_on_single_day_from_wind(indicator, date, log=False):
    """
    从wind上下载某个指定日期的指标

    @indicator (str): 指标名称,仅支持单个indicator传递
    @date ("%Y-%m-%d): 单个日期
    return: DataFrame，columns=['sec_id','indicator_name']
    """

    WindAPI.login(is_quiet=True)

    schema = SCHEMA[indicator]
    options = schema['kwargs']
    if schema["type"] == "时间序列":
        universe = get_index_contents(index_code="A", date=date, log=log)
        if universe is None:
            Logger.error("Fail to fetch stock lists on {}".format(date))
            raise ValueError
        options["tradeDate"] = date.replace("-", "")
    elif schema["type"] == "财报数据":
        # approx参数为True，保证财报日为非交易日的情形
        universe = get_index_contents(index_code="A", date=date, approx=True, log=log)
        if universe is None:
            Logger.error("Fail to fetch stock lists on: {}".format(date))
            raise ValueError
        options["rptDate"] = date.replace("-", "")
    else:
        Logger.error("Unrecognized indicator type: {}".format(schema["type"]))
        raise ValueError

    response = WDServer.wss(
        codes=",".join(universe),
        fields=indicator,
        options=options2str(options)
    )
    WindAPI.test_error(response)
    df = {field: response.Data[i] for i, field in enumerate(response.Fields)}
    df = pd.DataFrame(df, index=response.Codes).reset_index()
    df.columns = ["sec_id", indicator]
    return df

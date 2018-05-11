# -*- coding: utf-8 -*-

"""
indicator.py

写入指标原始数据

@author: Wu Yudi
@email: jasper.wuyd@gmail.com
@date: 2017.12.19

-------------------

FUNCTION LIST:
- update_single_indicator(indicator, trading_days=[], override=False, log=False)
- update_indicators(indicators=[], trading_days=[], override=False, log=False)
"""

import os
import traceback

from devkit.api import SqliteProxy, json2dict, Logger
from finkit.api import get_trading_days, get_report_days

from .. config import DB_PATH_LIB
from .. read import get_secs_indicator
from .. load import load_single_indicator_on_single_day_from_wind
from .. schema import get_schema, update_schema
from .. utils import classify_dates_by_year, create_table

DB_INDICATOR = DB_PATH_LIB["indicator"]


def update_single_indicator(indicator, trading_days=[], override=False, log=False):
    """
    更新单个indicator的指定日期列表的数据

    @indicator (str): 单个indicator的名称
    @trading_days ([%Y-%m-%d]): 日期列表
    @override (Bool): 是否覆盖原记录 默认为False 表示不覆盖
    @log (Bool): 是否打印log
    """

    if log:
        Logger.info("Updating indicator {}".format(indicator), "green")

    if indicator not in get_schema('indicator'):
        Logger.error("Unrecognized indicator: {}".format(indicator))
        raise ValueError

    if not trading_days:
        Logger.error("Empty date")
        raise ValueError

    with SqliteProxy(log=log) as proxy:
        date_classfier = classify_dates_by_year(trading_days)

        for year, date_list in date_classfier.items():
            path = os.path.join(DB_INDICATOR, '{}.db'.format(year))
            proxy.connect(path)

            if indicator not in proxy.list_tables:
                create_table(proxy, "indicator", indicator)

            # 判断已有数据
            if len(date_list) == 1:
                query = "SELECT DISTINCT(date) FROM {} WHERE date = '{}'".format(indicator, date_list[0])
            else:
                query = "SELECT DISTINCT(date) FROM {} WHERE date in {}".format(indicator, tuple(date_list))
            lookup = proxy.query_as_dataframe(query)
            lookup = set(lookup['date'].tolist())

            for date in date_list:
                if date in lookup and not override:  # 更新的日期已经存在于数据库时，不覆盖则跳过
                    if log:
                        Logger.warn("{} records on {} is existed.".format(indicator, date))
                    continue

                try:
                    df = load_single_indicator_on_single_day_from_wind(indicator=indicator, date=date)
                except Exception:
                    Logger.error("Error occurred when loading {} on {}".format(indicator, date))
                    raise ValueError

                if df is not None:  # 从Wind下载数据成功时
                    if date in lookup and override:  # 覆盖时删除原记录
                        proxy.execute("DELETE FROM [{}] WHERE date = '{}'".format(indicator, date))

                    df['date'] = date
                    try:
                        proxy.write_from_dataframe(df, indicator)
                    except Exception:
                        Logger.error("Error occurred when writing {} on {}".format(indicator, date))
                        traceback.print_exc()
                        raise ValueError
                    if log:
                        Logger.info("{} on {} is updated successfully".format(indicator, date))
                        
                else:  # 从wind提取数据失败时
                    Logger.error("Fail to fetch {} data on {}".format(indicator, date))
                    raise ValueError

    update_schema(db_name="indicator", sub_name=indicator)

    if log:
        Logger.info("indicator {} is updated.".format(indicator), color="green")
        Logger.info("------------------------------------------")


def update_indicators(indicators=[], trading_days=[], override=False, log=False):
    """
    更新多个indicator的指定日期列表的数据

    @indicators (list): indicator的名称构成的列表
    @trading_days ([%Y-%m-%d]): 日期列表
    @override (Bool): 是否覆盖原记录 默认为False 表示不覆盖
    @log (Bool): 是否打印log
    """

    SCHEMA = get_schema('indicator')
    if not indicators:
        indicators = list(SCHEMA.keys())

    start = trading_days[0]
    end = trading_days[-1]

    update_days_map = {
        "财报数据": set(get_report_days(start, end)),
        "时间序列": set(get_trading_days(start, end)),
    }

    for ind in indicators:
        if ind in SCHEMA:
            # 更新日期取交集
            itype = SCHEMA[ind]['type']
            update_days = [t for t in trading_days if t in update_days_map[itype]]
            if not update_days:
                Logger.warn("No valid days to update!")
            else:
                update_single_indicator(indicator=ind, trading_days=update_days, override=override, log=log)
        else:
            Logger.error("Unrecognized indicator: {}".format(ind))

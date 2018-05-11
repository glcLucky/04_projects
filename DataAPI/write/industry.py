# -*- coding: utf-8 -*-

"""
industry.py

写入行业数据

@author: Wu Yudi
@email: jasper.wuyd@gmail.com
@date: 2018.03.13

-------------------

FUNCTION LIST:
- update_industry(industry, trading_days=[], override=False, log=False)
- update_industry_to_sql(industry, trading_days, override, log)
- update_industry_to_json(industry, trading_days, override)
"""

import os
import shutil
import traceback
from datetime import datetime

import pandas as pd

from devkit.api import dict2json, Logger, SqliteProxy

from .. config import DB_PATH_LIB
from .. load import (
    load_secs_industry_sw_from_wind,
    load_secs_industry_gics_from_wind,
)
from .. schema import get_schema, save_schema, update_schema
from .. utils import classify_dates_by_year


DB_INDUSTRY = DB_PATH_LIB["industry"]
INDUSTRY_AS_SQL = ("A_SWL1", )
INDUSTRY_AS_JSON = ("H_GICSL1", "H_SWL1")

# 建立industry数据库名字到index_contents和载入函数的名字的map
INDEX_LOADER_MAP = {
    "A_SWL1": ("A", load_secs_industry_sw_from_wind),
    "H_SWL1": ("H", load_secs_industry_sw_from_wind),
    "H_GICSL1": ("H", load_secs_industry_gics_from_wind),
}


def update_industry(industry, trading_days=[], override=False, log=False):
    """
    从Wind更新某指数成分股申万一级行业数据

    @industry (str): 行业数据库名称
    @trading_days (['%Y-%m-%d']): 日期列表
    @override (Bool): 是否覆盖原记录 默认为False 表示不覆盖
    @log (Bool): 是否打印日志信息
    """

    Logger.info("Updating industry {}".format(industry), "green")

    if industry not in get_schema('industry'):
        Logger.error("Unrecognized industry: {}".format(industry))
        return

    if not trading_days:
        Logger.error("Empty date")
        raise ValueError

    if industry in INDUSTRY_AS_SQL:
        update_industry_to_sql(industry, trading_days, override, log)
    elif industry in INDUSTRY_AS_JSON:
        # 非sql数据强制更新，原有的会自动保存副本
        update_industry_to_json(industry, trading_days)
    else:
        Logger.error("Unrecognized industry: {}".format(industry))
        raise ValueError

    if log:
        Logger.info("industry/{} is updated.".format(industry), color="green")
        Logger.info("------------------------------------------")


def update_industry_to_sql(industry, trading_days, override, log):
    index_code, loader = INDEX_LOADER_MAP[industry]

    with SqliteProxy(log=log) as proxy:
        date_classfier = classify_dates_by_year(trading_days)

        for year, date_list in date_classfier.items():
            path = os.path.join(DB_INDUSTRY, '{}.db'.format(year))
            proxy.connect(path)

            if industry not in proxy.list_tables:
                create_table(proxy, "industry", industry)

            # 判断已有数据
            query = "SELECT DISTINCT(date) FROM [{}]".format(industry)
            lookup = proxy.query_as_dataframe(query)
            lookup = set(lookup['date'].tolist())

            for date in date_list:
                if date in lookup and not override:  # 更新的日期已经存在于数据库时，不覆盖则跳过
                    if log:
                        Logger.warn("{} records on {} is existed.".format(industry, date))
                    continue

                try:
                    df = {"sec_id": [], "industry": []}
                    info = loader(index_code, date, level=1)
                    for sec, ind in info.items():
                        df["sec_id"].append(sec)
                        df["industry"].append(ind)
                    df = pd.DataFrame(df)
                    df["date"] = date
                except Exception:
                    Logger.error("Error occurred when loading {} on {}".format(industry, date))
                    traceback.print_exc()
                    raise ValueError

                if df is not None:  # 从Wind下载数据成功时
                    try:
                        if date in lookup and override:  # 覆盖时删除原记录
                            proxy.execute("DELETE FROM [{}] WHERE date = '{}'".format(industry, date))

                        proxy.write_from_dataframe(df, industry)
                    except Exception:
                        Logger.error("Error occurred when writing {} on {}".format(industry, date))
                        traceback.print_exc()
                        raise ValueError

                    Logger.info("{} on {} is updated successfully".format(industry, date))
                else:  # 从wind提取数据失败时
                    Logger.error("Fail to fetch {} data on {}".format(industry, date))
                    traceback.print_exc()
                    raise ValueError

    update_schema("industry", industry)


def update_industry_to_json(industry, trading_days):
    try:
        date = trading_days[-1]
        index_code, loader = INDEX_LOADER_MAP[industry]
        info = loader(index_code, date, level=1)
    except Exception:
        Logger.error("Error occurred when loading {} on {}".format(industry, date))
        raise ValueError

    try:
        path = os.path.join(DB_INDUSTRY, '{}.json'.format(industry))
        copy_to = os.path.join(DB_INDUSTRY, '{}_backup.json'.format(industry))
        shutil.copy(path, copy_to)  # 保存副本，以防数据损坏
        dict2json(info, path, log=False)

        Logger.info("{} on {} is updated successfully".format(industry, date))
    except Exception:
        Logger.error("Error occurred when writing {} on {}".format(industry, date))
        raise ValueError

    # json files are different from sql, cannot use update_schema()
    # therefore update schema information explicitly
    try:
        now = datetime.now()
        schema = get_schema('industry')
        schema[industry]["begin date"] = ""
        schema[industry]["end date"] = now.strftime('%Y-%m-%d')
        schema[industry]['last update'] = now.strftime('%Y-%m-%d %H:%M:%S')
        save_schema(schema, 'industry')

        Logger.info("schema updated: {}".format(industry))
    except Exception:
        Logger.error("Error occurred when updating schema of {}".format(industry))
        traceback.print_exc()
        raise ValueError

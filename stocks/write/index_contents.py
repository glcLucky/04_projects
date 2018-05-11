# -*- coding: utf-8 -*-

"""
index_content.py

写入指数成分股的API

@author: Wu Yudi
@email: jasper.wuyd@gmail.com
@date: 2018.03.13

-------------------

FUNCTION LIST:
- update_index_contents(index_code, trading_days=[], override=False, log=False)
- update_index_contents_to_sql(index_code, trading_days, override, log=False)
- update_index_contents_to_csv(index_code, trading_days, override)
"""

import os
import shutil
import traceback
from datetime import datetime

from devkit.api import SqliteProxy, Logger

from .. config import DB_PATH_LIB
from .. load import (
    load_index_contents_from_wind,
    load_index_contents_and_weights_from_wind,
)
from .. read import get_index_contents_on_multidays
from .. schema import get_schema, save_schema, update_schema
from .. utils import classify_dates_by_year, create_table

DB_INDEX_CONTENTS = DB_PATH_LIB['index_contents']
IDXCONT_AS_SQL = ("A", "000016.SH", "000300.SH", "000905.SH")
IDXCONT_AS_CSV = ("H", "HSI.HI")
LOADER_MAP = {
    "A": load_index_contents_from_wind,
    "H": load_index_contents_from_wind,
    "HSI.HI": load_index_contents_from_wind,  # 恒生指数
    "000300.SH": load_index_contents_and_weights_from_wind,  # 沪深300
    "000016.SH": load_index_contents_and_weights_from_wind,  # 上证50
    "000905.SH": load_index_contents_and_weights_from_wind,  # 中证500
}


def update_index_contents(index_code, trading_days=[], override=False, log=False):
    """
    从Wind更新index_contents相关数据

    @index_code (str): 要更新的指标
    @trading_days (['%Y-%m-%d']): 传入的日期列表
    @override (Bool): 是否覆盖旧数据，默认为False，表示不覆盖
    @log (Bool): 是否打印log
    """

    Logger.info("Updating index_contents {}".format(index_code), "green")

    if index_code not in get_schema('index_contents'):
        Logger.error("Unrecognized index: {}".format(index_code))
        return

    if not trading_days:
        Logger.error("Empty date")
        raise ValueError

    if index_code in IDXCONT_AS_SQL:
        update_index_contents_to_sql(index_code, trading_days, override, log)
    elif index_code in IDXCONT_AS_CSV:
        # 非sql数据强制更新，原有的会自动保存副本
        update_index_contents_to_csv(index_code, trading_days)
    else:
        Logger.error("Unrecognized index code: {}".format(index_code))
        raise ValueError

    if log:
        Logger.info("index_content/{} is updated.".format(index_code), color="green")
        Logger.info("------------------------------------------")


def update_index_contents_to_sql(index_code, trading_days, override, log=False):
    with SqliteProxy(log=log) as proxy:
        date_classfier = classify_dates_by_year(trading_days)

        for year, date_list in date_classfier.items():
            path = os.path.join(DB_INDEX_CONTENTS, '{}.db'.format(year))
            proxy.connect(path)
            if index_code not in proxy.list_tables:
                create_table(proxy, "index_contents", index_code)

            # 判断已有数据
            query = "SELECT DISTINCT(date) FROM [{}]".format(index_code)
            lookup = proxy.query_as_dataframe(query)
            lookup = set(lookup['date'].tolist())

            for date in date_list:
                if date in lookup and not override:  # 更新的日期已经存在于数据库时，不覆盖则跳过
                    if log:
                        Logger.warn("{} records on {} is existed.".format(index_code, date))
                    continue

                try:
                    loader = LOADER_MAP[index_code]
                    df = loader(index_code, date)
                    df['date'] = date
                except Exception:
                    Logger.error("Error occurred when loading {} on {}".format(index_code, date))
                    raise ValueError

                if df is not None:  # 从Wind下载数据成功时
                    try:
                        if date in lookup and override:  # 覆盖时删除原记录
                            proxy.execute("DELETE FROM [{}] WHERE date = '{}'".format(index_code, date))

                        proxy.write_from_dataframe(df, index_code)
                    except Exception:
                        Logger.error("Error occurred when writing {} on {}".format(index_code, date))
                        traceback.print_exc()
                        raise ValueError

                    Logger.info("{} on {} is updated successfully".format(index_code, date))
                else:  # 从wind提取数据失败时
                    Logger.error("Fail to fetch {} data on {}".format(index_code, date))
                    raise ValueError

    update_schema('index_contents', index_code)


def update_index_contents_to_csv(index_code, trading_days, override):
    try:
        date = trading_days[-1]
        df = loader(index_code, date)
        loader = LOADER_MAP[index_code]
    except Exception:
        Logger.error("Error occurred when loading {}".format(index_code))
        raise ValueError

    try:
        path = os.path.join(DB_INDEX_CONTENTS, '{}.csv'.format(index_code))
        copy_to = os.path.join(DB_INDEX_CONTENTS, '{}_backup.csv'.format(index_code))
        shutil.copy(path, copy_to)  # 保存副本，以防数据损坏
        df.to_csv(path, encoding="utf-8", index=False)

        Logger.info("{} on {} is updated successfully".format(index_code, date))
    except Exception:
        Logger.error("Error occurred when writing {}".format(index_code))
        traceback.print_exc()
        raise ValueError

    # csv files are different from sql, cannot use update_schema()
    # therefore update schema information explicitly
    try:
        now = datetime.now()
        schema = get_schema('index_contents')
        schema[index_code]["begin date"] = ""
        schema[index_code]["end date"] = now.strftime('%Y-%m-%d')
        schema[index_code]['last update'] = now.strftime('%Y-%m-%d %H:%M:%S')
        save_schema(schema, 'index_contents')

        Logger.info("schema updated: {}".format(index_code))
    except Exception:
        Logger.error("Error occurred when updating schema of {}".format(index_code))
        traceback.print_exc()
        raise ValueError

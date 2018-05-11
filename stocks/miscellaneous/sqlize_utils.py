# -*- coding: utf-8 -*-

import os
import traceback

import pandas as pd

from devkit.api import json2dict, SqliteProxy, Logger

from .. config import DB_PATH, DB_PATH_LIB
from .. schema import get_schema
from .. utils import (
    classify_dates_by_year,
    create_db_01, create_db_02, create_db_03,
    listdir_advanced,
)

DB_CREATOR_MAP = {
    "indicator": create_db_01,
    "factor": create_db_01,
    "index_contents": create_db_02,
}


def delete_records(conds):
    """从数据库中删除满足指定条件的记录"""

    with SqliteProxy(log=True) as proxy:
        for db_name, db_path in DB_PATH_LIB.items():
            for db_file in listdir_advanced(db_path, "db"):
                db_path = os.path.join(db_path, db_file)
                proxy.connect(db_path)
                for table in proxy.list_tables:
                    try:
                        proxy.execute("DELETE FROM [{}] WHERE {}".format(table, conds))
                    except Exception:
                        traceback.print_exc()
                        continue


def sqlize_db_industry(subdb):
    """
    将 industry sql化

    @subdb (str): 子数据库名 
    """

    db_path = DB_PATH_LIB['industry']
    subdb_path = os.path.join(db_path, subdb)
    trading_days = listdir_advanced(subdb_path, 'json', strip_suffix=True)
    with SqliteProxy(log=False) as proxy:
        for year, dates in classify_dates_by_year(trading_days).items():
            path = os.path.join(db_path, '{}.db'.format(year))
            proxy.connect(path)
            if subdb not in proxy.list_tables:
                create_db_03(proxy, subdb)

            for date in dates:
                js = json2dict(os.path.join(subdb_path, '{}.json'.format(date)))
                df = pd.DataFrame(list(js.items()), columns=['sec_id', 'industry'])
                df['date'] = date
                try:
                    proxy.write_from_dataframe(df, "A_SWL1")
                except Exception:
                    Logger.error("Error occurred when sqlizing {} on {}.".format(subdb, date))
                    traceback.print_exc()


def sqlize_db(db_name, subdb_list=[]):
    """将数据库sql化"""

    if not subdb_list:
        subdb_list = list(get_schema(db_name).keys())
    else:
        subdb_list = [s for s in subdb_list if s in get_schema(db_name)]

    db_path = os.path.join(DB_PATH, db_name)

    with SqliteProxy(log=False) as proxy:
        for subdb in subdb_list:
            Logger.info("SQLing {}/{}".format(db_name, subdb), "green")

            subdb_path = os.path.join(db_path, subdb)
            trading_days = listdir_advanced(subdb_path, 'csv', strip_suffix=True)
            for year, dates in classify_dates_by_year(trading_days).items():
                path = os.path.join(db_path, '{}.db'.format(year))
                proxy.connect(path)

                if subdb not in proxy.list_tables:
                    creator = DB_CREATOR_MAP[db_name]
                    creator(proxy, subdb)

                for date in dates:
                    df = pd.read_csv(os.path.join(subdb_path, '{}.csv'.format(date)))
                    df['date'] = date
                    try:
                        proxy.write_from_dataframe(df, subdb)
                    except Exception:
                        Logger.error("Error occurred when sqlizing {} on {}.".format(subdb, date))
                        traceback.print_exc()

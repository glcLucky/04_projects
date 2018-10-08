# -*- coding: utf-8 -*-

"""
schema.py

数据库信息

@author: Jasper Gui
@email: jasper.gui@outlook.com
@date: 2017.12.11

------------------
FUNCTIONS LIST:
- get_schema(db_name)
- show_dbs_composition(db_names)
- show_db_info(db_name)
"""

import os

from devkit.api import json2dict, dict2json
from .. config import (DB_PATH, DB_PATH_LIB)

SCHEMA_PATHS = {sub_db: os.path.join(DB_PATH_LIB[sub_db], 'schema') for sub_db in DB_PATH_LIB}


def get_schema(db_name):
    """
    获得某个数据库schema的相关信息

    @db_name (int): 数据库名称
    @return dict of schema
    """

    schema = json2dict(SCHEMA_PATHS[db_name])
    return schema


def save_schema(schema, db_name):
    dict2json(schema, SCHEMA_PATHS[db_name], log=False)


def show_dbs_composition(db_names):
    """
    展示某个数据的构成

    @db_names (int): 数据库名称
    """

    for db in db_names:
        schema = get_schema(db)
        print("{}下有如下子数据".format(db))
        for sub_db in schema:
            print(sub_db)
        print("\n")


def show_db_info(db_name):
    """
    打印指定数据库的schema相关信息

    @db_names (int): 数据库名称
    """

    schema = get_schema(db_name)
    print("数据库 [{}] 架构信息：\n".format(db_name))
    for sub_db, sub_schema in schema.items():
        print("子数据库 [{}]".format(sub_db))
        print("    说明：{}".format(sub_schema["explanation"]))
        print("    开始时间：{}".format(sub_schema["begin date"]))
        print("    结束时间：{}".format(sub_schema["end date"]))
        print("    最后更新：{}\n".format(sub_schema["last update"]))

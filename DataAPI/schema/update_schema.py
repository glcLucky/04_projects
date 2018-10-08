# -*- coding: utf-8 -*-

"""
update_schema.py

更新各因子库的schema

@author: Gui lichao
@email:
@date: 2017.12.19

-------------------
FUNCTIONS LIST：
- update_indicator_schema(indicator)
- update_factor_schema(factor)
- update_factor_return_schema(factor)

"""

import os
from datetime import datetime

import pandas as pd

from devkit.api import dict2json, json2dict, Logger

from .. config import DB_PATH_LIB
from .. config import DB_PATH
from .. utils import (
    get_date_lists_in_table,
)


def update_schema(db_name, sub_name):
    """
    更新schema相关的begin date，end date, last update 适用于非factor_return相关的数据库

    @db_name (str): db的名称 eg. FACTOR 排除factor_return
    @sub_name (str): db中各子数据库的名称 eg. VALUE GROWTH
    """

    schema = json2dict(os.path.join(DB_PATH_LIB[db_name], 'schema'))

    assert sub_name

    date_list = get_date_lists_in_table(DB_PATH_LIB[db_name], sub_name)

    schema[sub_name]['begin date'] = date_list[0]
    schema[sub_name]['end date'] = date_list[-1]
    schema[sub_name]['last update'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    Logger.info("schema updated: {}".format(sub_name))
    dict2json(schema, os.path.join(DB_PATH_LIB[db_name], 'schema'), log=False)
    a = pd.DataFrame(schema).T
    col_names = ['aspect', 'type', 'begin date', 'end date', 'last update', 'col_names', 'field', 'kwargs', 'explanation']
    b = a.reindex(columns=col_names).reset_index().rename(columns={'index': 'indicator'}).sort_values(['type', 'aspect', 'field'])
    b.to_csv(os.path.join(DB_PATH_LIB[db_name], 'schema.csv'), index=False)


def update_factor_return_schema(factor):
    """
    更新factor_return的schema相关的begin date，end date, last update

    @factor (str): factor的名称
    """

    schema = json2dict(os.path.join(DB_PATH_LIB['factor_return'], 'schema'))

    filepath = os.path.join(DB_PATH_LIB['factor_return'], "{}.csv".format(factor))
    df = pd.read_csv(filepath, encoding="utf-8")["date"]
    schema[factor]['begin date'] = df.min()

    schema[factor]['end date'] = df.max()

    schema[factor]['last update'] = \
        datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    Logger.info("schema updated: {}".format(factor))
    dict2json(schema, os.path.join(DB_PATH_LIB['factor_return'], 'schema'), log=False)

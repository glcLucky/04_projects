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
from .. config import SCHEMA_PATH


def get_schema(db_name):
    """
    获得某个数据库schema的相关信息

    @db_name (int): 数据库名称
    @return dict of schema
    """
    path = os.path.join(SCHEMA_PATH, "schema_{}.json".format(db_name))
    schema = json2dict(path)
    return schema


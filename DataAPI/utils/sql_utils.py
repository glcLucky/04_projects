# -*- coding: utf-8 -*-

"""
sql_utils.py

sql数据库工具函数

@author: Jasper Gui
@email: jasper.gui@outlook.com
@date: 2018.03.13

-------------------

FUNCTION LIST:
- create_table(proxy, db, table_name)
- generate_table_template(db, table_name)
"""

import os
import traceback

from devkit.api import SqliteProxy, Logger


def create_table(proxy, db, table_name):
    template = generate_table_template(db, table_name)
    proxy.create_table(table_name, template)
    proxy.create_index("{}_index".format(table_name), ["date", "sec_id"], table_name, is_unique=True)


def generate_table_template(db, table_name):
    """生成数据库建表模板"""

    if db in ("indicator", "factor"):
        template = [
            ("date", "CHAR(10)", False, False),
            ("sec_id", "TEXT", False, False),
            (table_name, "REAL", False, True),
        ]
    elif db == "index_contents":
        if table_name == "A_SWL1":
            template = [
                ("date", "CHAR(10)", False, False),
                ("sec_id", "TEXT", False, False),
                ("sec_name", "TEXT", False, False),
            ]
        elif table_name in ('000016.SH', '000300.SH', '000905.SH'):
            template = [
                ("date", "CHAR(10)", False, False),
                ("sec_id", "TEXT", False, False),
                ("sec_name", "TEXT", False, False),
                ("weight", "REAL", False, False),
            ]
        else:
            Logger.error("Unrecognized table name: {}".format(table_name))
            raise ValueError
    elif db == "industry":
        template = [
            ("date", "CHAR(10)", False, False),
            ("sec_id", "TEXT", False, False),
            ("industry", "TEXT", False, True),
        ]
    else:
        Logger.error("Unrecognized db name: {}".format(db))
        raise ValueError
    return template

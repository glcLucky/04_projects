# -*- coding: utf-8 -*-

"""
sql_utils.py

sql数据库工具函数

@author: Wu Yudi
@email: jasper.wuyd@gmail.com
@date: 2018.03.13

-------------------

FUNCTION LIST:
- create_table(proxy, db, table_name)
- generate_table_template(db, table_name)
"""

import os
import traceback

from devkit.api import MySQLProxy, Logger
from .. config import (USER, PASSWORD)


def get_unique_datelist_from_table(database, table, date_name="date", log=False):
    """
    获取指定数据库指定表的不同日期列表 升序排列
    @database <str>: 数据库名称
    @talbe <str>: 表名称
    @date_name <str>: 日期变量的名字 默认为date
    @return: 返回升序排列的字符串日期列表 %Y-%m-%d
    """

    with MySQLProxy(log=log) as proxy:
        output = {}
        proxy.connect(USER, PASSWORD, database)
        datelist = proxy.query_as_dataframe("SELECT DISTINCT {} FROM {}".format(date_name, table))
        datelist = datelist[date_name].apply(lambda x: str(x)).tolist()
        return datelist

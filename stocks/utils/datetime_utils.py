# -*- coding: utf-8 -*-

"""
datetime_utils.py

日期处理工具函数

@author: Jasper Gui
@email: jasper.gui@outlook.com
@date: 2018.03.08

-------------------

FUNCTION LIST:
- get_previous_report_day(date)
- get_previous_existed_day_in_table(path, date, table_name)
- get_date_lists_in_table(db_path, table_name)
- classify_dates_by_year(dates)
"""

import os
import traceback
from datetime import date as Date
from datetime import datetime, timedelta

from devkit.api import SqliteProxy

from . file_utils import listdir_advanced


def get_previous_report_day(date):
    """
    获得当前日期的上一个季末日期
    :param date : (str, %Y-%m-%d) 给定的日期
    :return:str,%Y-%m-%d 返回给定日期下上一个季末的日期
    """

    if date[5:] in ['03-31', '06-30', '09-30', '12-31']:
        return date
    else:
        date_tm = datetime.strptime(date, "%Y-%m-%d")
        if date_tm.month <= 3:
            month = 1
        elif date_tm.month <= 6:
            month = 4
        elif date_tm.month <= 9:
            month = 7
        else:
            month = 10
        first = Date(year=date_tm.year, month=month, day=1)
        lastmonth = first - timedelta(days=1)
        output = datetime.strftime(lastmonth, "%Y-%m-%d")
        return output


def get_previous_existed_day_in_table(date, db_path, table_name):
    """
    获取数据库特定表中已存在交易日中，比date小且距date最近的交易日

    :param file_dir: <str> 文件夹路径
    :param date: <%Y-%m-%d> 日期名称
    :return: last_factor_day <%Y-%m-%d>
    """

    year = date[:4]
    output = None
    while True:
        filepath = os.path.join(db_path, '{}.db'.format(year))
        if not os.path.exists(filepath):
            break

        with SqliteProxy(log=False) as proxy:
            proxy.connect(filepath)
            if table_name not in proxy.list_tables:
                break

            try:
                query = "SELECT MAX(date) as date FROM [{}] WHERE date < '{}'".format(table_name, date)
                df = proxy.query_as_dataframe(query)
            except Exception:
                traceback.print_exc()
                break

            output = df.at[0, 'date']
            if output:
                break
        year = str(int(year)-1)

    return output


def get_date_lists_in_table(db_path, table_name):
    """获取某张表中已有的日期，该表存在于多个db中，返回一个list"""

    datelist = []
    with SqliteProxy(log=False) as proxy:
        for db in listdir_advanced(db_path, "db"):
            path = os.path.join(db_path, db)
            proxy.connect(path)

            if table_name in proxy.list_tables:
                query = "SELECT DISTINCT(date) FROM [{}]".format(table_name)
                try:
                    df = proxy.query_as_dataframe(query)
                    datelist += df['date'].tolist()
                except Exception:
                    traceback.print_exc()
    return sorted(datelist)


def classify_dates_by_year(dates):
    """
    按年划分日期列表
    @dates (list): 日期列表
    @return {year: [dates in year]}
    """

    output = {}
    for date in dates:
        year = date[:4]
        if year in output:
            output[year].append(date)
        else:
            output[year] = [date]
    return output

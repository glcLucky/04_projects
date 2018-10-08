# -*- coding: utf-8 -*-

"""
datetime_utils.py

时间处理相关工具函数

@author: Lichao Gui
@email:
@date: 2017.12.11

---------------

FUNCTION LIST:
- df_sampling(df, nsamples, force=True)
"""
import datetime
from dateutil.relativedelta import relativedelta


def char2datetime(date_in, format="%Y-%m-%d"):
    """
    将"YYYY-mm-dd"形式的日期字符串转换为datetime.date
    """
    if len(date_in) == 0:
        return None
    num = datetime.datetime.strptime(date_in, format).date()
    return num


def date2char(date_in, format="%Y-%m-%d"):
    """
    将"YYYY-mm-dd"形式的日期转换为日期字符串
    """
    str_date = datetime.datetime.strftime(date_in, format)
    return str_date


def timedelta(delta):
    """
    将数值转换为对应周期
    @delta<dict>: {周期： 数值}
    """
    return relativedelta(**delta)


def get_available_report_day(date):
    """
    获得当前日期对应的可行的财报日 规则如下:
    2010-01-01 -- 2010-04-31 -> 2009/9/30  2010-05-01 -- 2010-07-31 -> 2009/12/31
    2010-08-01 -- 2010-09-30 -> 2010/3/31  2010-10-01 -- 2010-10-31 -> 2010/6/30
    2010-11-01 -- 2010-12-31  -> 2010/9/30
    :param date : (str, %Y-%m-%d) 给定的日期
    :return:str,%Y-%m-%d 返回给定日期下上一个季末的日期
    """

    date_tm = datetime.datetime.strptime(date, "%Y-%m-%d")
    if 1 <= date_tm.month <= 4:
        date_tm = datetime.datetime(date_tm.year - 1, 9, 30).date()
    elif 5 <= date_tm.month <= 7:
        date_tm = datetime.datetime(date_tm.year - 1, 12, 31).date()
    elif 8 <= date_tm.month <= 9:
        date_tm = datetime.datetime(date_tm.year, 3, 31).date()
    elif date_tm.month == 10:
        date_tm = datetime.datetime(date_tm.year, 6, 30).date()
    elif 11 <= date_tm.month <= 12:
        date_tm = datetime.datetime(date_tm.year, 9, 30).date()
    else:
        print("Invalid date!!")
    output = datetime.datetime.strftime(date_tm, "%Y-%m-%d")
    return output


def date2week(date, format="%Y-%m-%d"):
    """
    将指定格式的日期转换为星期
    """
    date = datetime.datetime.strptime(date, format)
    week_day_dict = {
        0: '星期一',
        1: '星期二',
        2: '星期三',
        3: '星期四',
        4: '星期五',
        5: '星期六',
        6: '星期天',
    }
    day = date.weekday()
    return week_day_dict[day]

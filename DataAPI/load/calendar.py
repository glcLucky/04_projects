# -*- coding: utf-8 -*-

"""
calendar.py

从wind数据库载入原始calendar数据

@author: Jasper Gui
@email: jasper.gui@outlook.com
@date: 2018.03.08

-------------------

"""

import os

from devkit.api import Logger

import WindAPI
import pandas as pd


def load_calendar_from_wind(start_date, end_date):
    """从Wind载入交易日历数据，注意start必须是月初，end必须是月末，不然数据不对
    @start_date ("%Y-%m-%d"): 开始日日期 必须是月初日期
    @end_date ("%Y-%m-%d"): 结束日日期 必须是月月末日期
    """
    start_date = start_date.replace("-", "")
    end_date = end_date.replace("-", "")
    WindAPI.login(is_quiet=True)

    response = WindAPI.WDServer.tdays(start_date, end_date, "Days=Alldays")
    alldays = [dt.strftime("%Y-%m-%d") for dt in response.Data[0]]

    calendar = pd.DataFrame({"date": alldays}).set_index("date")
    calendar["is_trading_day"] = 0
    calendar["is_weekly_last_trading_day"] = 0
    calendar["is_monthly_last_trading_day"] = 0
    calendar["is_report_day"] = 0

    response = WindAPI.WDServer.tdays(start_date, end_date, "Period=D")
    trading_days = [dt.strftime("%Y-%m-%d") for dt in response.Data[0]]
    calendar.loc[trading_days, "is_trading_day"] = 1

    response = WindAPI.WDServer.tdays(start_date, end_date, "Period=W")
    trading_days = [dt.strftime("%Y-%m-%d") for dt in response.Data[0]]
    calendar.loc[trading_days, "is_weekly_last_trading_day"] = 1

    response = WindAPI.WDServer.tdays(start_date, end_date, "Period=M")
    trading_days = [dt.strftime("%Y-%m-%d") for dt in response.Data[0]]
    calendar.loc[trading_days, "is_monthly_last_trading_day"] = 1

    for date in calendar.index:
        if date[-5:] in ("03-31", "06-30", "09-30", "12-31"):
            calendar.at[date, "is_report_day"] = 1

    calendar = calendar.reset_index()
    return calendar

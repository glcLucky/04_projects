# -*- coding: utf-8 -*-

"""
calendar.py
写入交易日原始数据

@author: Jasper Gui
@email: jasper.gui@outlook.com
@date: 2017.12.29

-------------------

"""

import traceback
import os

from devkit.api import Logger, SqliteProxy
from .. load import load_calendar_from_wind
from .. config.path import DB_PATH_LIB
from .. read import get_trading_days

DB_CALENDAR_PATH = DB_PATH_LIB["calendar"]


def update_calendar(start_date, end_date, log=False):
    """
    从Wind更新calendar相关数据 每次更新将删除原有所有数据 更新到当前区间

    @start_date ("%Y-%m-%d"): 开始日日期 必须是月初日期
    @end_date ("%Y-%m-%d"): 结束日日期 必须是月月末日期
    @log (Bool): 是否打印log
    """

    Logger.info("Updating calendar ...", "green")

    max_existed_date = get_trading_days
    with SqliteProxy(log=log) as proxy:
        proxy.connect(os.path.join(DB_CALENDAR_PATH, "calendar.db"))
        proxy.execute("DELETE FROM calendar")
        try:
            df = load_calendar_from_wind(start_date, end_date)
        except Exception:
            Logger.error("Error occurred when loading")
            raise ValueError
        try:
            proxy.write_from_dataframe(df, "calendar")
        except Exception:
            Logger.error("Error occurred when writing dataframe into sqlite db")
            traceback.print_exc()
            raise ValueError
    if log:
        Logger.info("calendar was updated from {} to {}".format(start_date, end_date), color="green")
        Logger.info("------------------------------------------")
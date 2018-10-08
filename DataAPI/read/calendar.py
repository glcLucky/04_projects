# -*- coding: utf-8 -*-

"""
calendar.py

读取交易日相关的API

@author: Jasper Gui
@email: jasper.gui@outlook.com
@date: 2018.03.13
"""


import os
import traceback

import pandas as pd
from devkit.api import json2dict, Logger, SqliteProxy
from .. config.path import DB_PATH_LIB
DB_CALENDAR_PATH = DB_PATH_LIB["calendar"]


def get_trading_days(start, end, format=lambda x: x, log=False):
    db = SqliteProxy(log=log)
    db.connect(os.path.join(DB_CALENDAR_PATH, "calendar.db"))
    query = ("SELECT date FROM calendar WHERE date BETWEEN '{}' AND '{}'"
             "AND is_trading_day = 1").format(start, end)
    date = [format(r[0]) for r in db.execute(query)]
    db.close()
    return date


def get_weekly_last_trading_days(start, end, format=lambda x: x, log=False):
    db = SqliteProxy(log=log)
    db.connect(os.path.join(DB_CALENDAR_PATH, "calendar.db"))

    query = ("SELECT date FROM calendar WHERE date BETWEEN '{}' AND '{}'"
             "AND is_weekly_last_trading_day = 1").format(start, end)
    date = [format(r[0]) for r in db.execute(query)]

    db.close()

    return date


def get_monthly_last_trading_days(start, end, format=lambda x: x, log=False):
    db = SqliteProxy(log=log)
    db.connect(os.path.join(DB_CALENDAR_PATH, "calendar.db"))

    query = ("SELECT date FROM calendar WHERE date BETWEEN '{}' AND '{}'"
             "AND is_monthly_last_trading_day = 1").format(start, end)
    date = [format(r[0]) for r in db.execute(query)]

    db.close()

    return date


def get_weekly_and_monthly_last_trading_days(start, end, format=lambda x: x, log=False):
    db = SqliteProxy(log=log)
    db.connect(os.path.join(DB_CALENDAR_PATH, "calendar.db"))

    query = ("SELECT date FROM calendar WHERE (date BETWEEN '{}' AND '{}')"
             "AND (is_weekly_last_trading_day = 1 "
             "OR is_monthly_last_trading_day = 1)")
    query = query.format(start, end)
    date = [format(r[0]) for r in db.execute(query)]

    db.close()

    return date


def get_report_days(start, end, format=lambda x: x, log=False):
    db = SqliteProxy(log=log)
    db.connect(os.path.join(DB_CALENDAR_PATH, "calendar.db"))

    query = ("SELECT date FROM calendar WHERE date BETWEEN '{}' AND '{}'"
             "AND is_report_day = 1").format(start, end)
    date = [format(r[0]) for r in db.execute(query)]

    db.close()

    return date

# -*- coding: utf-9 -*-

"""
indicator.py
读取indicator

"""
from devkit.api import Logger
from devkit.api import MySQLProxy
from .. config import (
    ROOT,
    PASSWORD,
)


def get_features_fr(features=[], sec_ids=[], trading_days=[]):
    """
    从mysql数据库中读取指定日期指定股票指定指标的数据
    @features <list>: 财务指标名称列表 
    @sec_ids <list>: 股票代码列表
    @trading_days <list>: 日期列表
    """
    conn = MySQLProxy()
    conn.connect(ROOT, PASSWORD, "indicator")
    query = "SELECT {} FROM report_variables WHERE sec_id in {} and date in {}".format(
        tuple(features), tuple(sec_ids), tuple(trading_days))
    output = conn.queryquery_as_dataframe(query)
    return output

# # -*- coding: utf-8 -*-

# """
# factor.py
# 写入因子原始数据

# @author: Gui lichao
# @date: 2018.04.08

# -------------------

# FUNCTION LIST:
# - update_single_factor(factor, trading_days=[], override=False, log=False)
# - update_factors(factors=[], trading_days=[], override=False, log=False)
# """

# import os
# import traceback

# from devkit.api import json2dict, Logger, SqliteProxy

# from .. load import load_single_factor_on_single_day
# from .. utils import classify_dates_by_year
# from .. schema import get_schema, update_schema
# from .. config import (USER, PASSWORD)
# from .. utils import create_table

# DB_FACTOR = os.path.join(DB_PATH, "factor")


# def update_single_factor(factor, trading_days=[], log=False):
#     """
#     更新单个factor的指定日期列表的数据

#     @factor (str): factor名称
#     @trading_days ([%Y-%m-%d]): 日期列表
#     @override (Bool): 是否覆盖原记录，默认为False，表示不覆盖
#     @log (Bool): 是否打印log
#     """

#     Logger.info("Updating factor {}".format(factor), "green")

#     if factor not in get_schema('factor'):
#         Logger.error("Unrecognized factor: {}".format(factor))
#         raise ValueError

#     if not trading_days:
#         Logger.error("Empty date")
#         raise ValueError

#     with MySQLProxy(log=log) as proxy:
#         output = {}
#         proxy.connect(USER, PASSWORD, "factor")
#         try:
#             df = load_single_factor(factor=factor, trading_days=trading_days)
#         except Exception:
#             Logger.error("Error occurred when loading {}".format(factor))
#             traceback.print_exc()
#         if df is not None:
#             try:
#                 proxy.write_from_dataframe(df, factor)
#             except Exception:
#                 Logger.error("Error occurred when writing {}".format(factor))
#                 traceback.print_exc()
#                 raise ValueError
#             if log:
#                 Logger.info("{} is updated successfully".format(factor))
#         else:
#             Logger.error("Fail to calculate the factor: {}".format(factor))
#             raise ValueError

#     if log:
#         Logger.info("factor {} is updated.".format(factor), color="green")
#         Logger.info("------------------------------------------")


# def update_factors(factors=[], trading_days=[], log=False):
#     """
#     更新多个factor的指定日期列表的数据

#     @factors (<list>):factor名称构成的列表
#     @trading_days ([%Y-%m-%d]): 日期列表
#     @override (<Bool>): 是否覆盖原记录 默认为False 表示不覆盖
#     @log (<Bool>): 是否打印log
#     """

#     SCHEMA = get_schema("factor")
#     if not factors:
#         factors = sorted(SCHEMA, key=lambda x: SCHEMA[x]["level"])

#     for fac in factors:
#         if fac in SCHEMA:
#             update_single_factor(factor=fac, trading_days=trading_days, override=override, log=log)
#         else:
#             Logger.error("Unrecognized factor: {}".format(fac))
#             Logger.info("------------------------------------------")

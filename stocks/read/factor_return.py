# -*- coding: utf-8 -*-

"""
factor_return.py

factor_return相关的API

@author: Gui lichao
@email:
@date: 2018.01.16

-------------------

FUNCTION LIST:
- get_factor_return_daily(factor_return_name, trading_days="")
- get_factor_return_cum(factor_return_name, trading_days="")
"""

import os
import matplotlib.pyplot as plt
import seaborn
seaborn.set_style("darkgrid")

from devkit.api import (
    open_csv_as_df,
    json2dict,
    Logger
)

from .. config import DB_PATH
from .. schema import get_schema

DB_FACTOR_RETURN_PATH = os.path.join(DB_PATH, "factor_return")


def get_factor_return_daily(factor_return_name, trading_days=[]):
    """
    从本地数据库中获取某段日期某个factor_return的日收益率

    @factor_return_name (str): factor名称
    @trading_days (['%Y-%m-%d']): 日期列表
    :return: DataFrame, index: date, columns: [sec_id, group01-group10, factor]
    """

    if factor_return_name not in get_schema("factor_return"):  # 判断所给定的factor_return是否存在本地factor库中
        Logger.error("{} is not in FACTOR_RETURN library".format(
            factor_return_name))
        return
    else:
        filepath = os.path.join(DB_FACTOR_RETURN_PATH, "{}.csv".format(factor_return_name))
        df_info = open_csv_as_df(filepath, validate=True)

        if not trading_days:
            output = df_info.copy()
        else:
            output = df_info[df_info.date.isin(trading_days)]
            not_found_dates = set(trading_days) - set(output["date"].tolist())
            if not_found_dates:
                Logger.warn(
                    "Following dates are invalid: {}".format(not_found_dates))
                return
        output = output.set_index(['date'])
        return output


def get_factor_return_cum(factor_return_name, trading_days=[]):
    """
    从本地数据库中获取某段日期某个factor_return的累计收益率

    @factor_return_name (str): factor名称
    @trading_days (['%Y-%m-%d']): 日期列表
    :return: DataFrame, index: date, columns: [sec_id, group01-group10, factor]
    """

    if factor_return_name not in get_schema("factor_return"):  # 判断所给定的factor是否存在本地factor库中
        Logger.error("{} is not in FACTOR_RETURN library".format(factor_return_name))
        return

    else:
        filepath = os.path.join(DB_FACTOR_RETURN_PATH,
                                "{}.csv".format(factor_return_name))
        df_info = open_csv_as_df(filepath, validate=True)

        if not trading_days:
            output = df_info.copy()
        else:
            output = df_info[df_info.date.isin(trading_days)]
            not_found_dates = set(trading_days) - set(output["date"].tolist())
            if not_found_dates:
                Logger.warn(
                    "Following dates are invalid: {}".format(not_found_dates))
                return
        output = output.set_index('date')
        #  基于复利求累计收益率
        for i in range(output.shape[0]):
            if i == 0:
                output.iloc[i, :] = 1.  # (1 + output.iloc[i, :])
            else:
                output.iloc[i, :] = output.iloc[i-1, :] * (1 + output.iloc[i, :])

        return output


def plot_single_factor_return_cum(factor_return_name_list, trading_days=[], save_plot_path=""):
    """
    绘制多个factor_return的累计收益率图并存放于指定位置

    @factor_return_name_list (list): factor列表
    @trading_days （['%Y-%m-%d']) : 日期列表
    @save_plot_path (str): 存放路径
    """

    if len(factor_return_name_list) == 0:
        factor_return_name_list = list(get_schema("factor_return").keys())

    for factor_return_name in factor_return_name_list:
        df = get_factor_return_cum(factor_return_name=factor_return_name, trading_days=trading_days)
        fig = plt.figure(figsize=(12, 6))
        ax = plt.subplot(111)
        df.iloc[:, :10].plot(ax=ax)
        ax.set_title("{}累计收益".format(factor_return_name))
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        if save_plot_path != "":
            picfile = os.path.join(save_plot_path, "{}.png".format(factor_return_name))
            plt.savefig(picfile)
            print("plot is saved to: {}".format(picfile))

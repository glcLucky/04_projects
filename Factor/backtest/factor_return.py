  # -*- coding: utf-8 -*-

"""
factor_return.py
对index/factor进行回测

"""
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

from devkit.api import Logger, listdir_advanced
from .. read import get_secs_index, get_secs_index_std
from .. config.path import PROJECT_FILES_PATH
from .. utils import paired_ttest


def get_single_index_daily_return(index_std, trading_days, cycle, groups=10, save_plot=True, save_daily=True, save_cum=True):
    """
    对单个index_std进行回测，输出单日收益表
    @index_std <str>: index名称
    @trading_days <list of date>: 回测时间段 时间是datetime格式
    @cycle <int>: 以天为单位的周期
    @groups <int>: 分组个数 默认为10
    """

    if len(trading_days) == 0:
        Logger.error("Empty date!!")

    # 根据周期计算会用到的时间点
    trading_days = sorted(trading_days)
    selected_days = []
    for i in range(cycle, len(trading_days), cycle):
        selected_days.append(trading_days[i])
    selected_days = list(map(str, selected_days))
    # 一次性获取回测周期的前复权收盘价和index_std
    df_close = get_secs_index(index='close', sec_ids=[], trading_days=selected_days)
    df_index = get_secs_index_std(index_std=index_std, sec_ids=[], trading_days=selected_days)
    df_daily = pd.DataFrame()
    for i in range(len(selected_days) - 1):
        date_now = selected_days[i]
        date_next = selected_days[i + 1]
        index_now = df_index[df_index.date == date_now]
        close_now = df_close[df_close.date == date_now].rename(columns={'close': 'close_now'})
        del close_now['date']
        close_next = df_close[df_close.date == date_next].rename(columns={'close': 'close_next'})
        del close_next['date']
        df_all = index_now.merge(close_now, how='inner', on=['sec_id'])
        df_all = df_all.merge(close_next, how='inner', on=['sec_id'])
        df_all = df_all.sort_values(by=[index_std])
        df_all['return_rate'] = df_all['close_next'] / df_all['close_now'] - 1
        # 分组 如果不能整分 则将多余的归为最后一组 多余的个数不会超过分组个数
        df_all['group'] = np.nan
        group_index = df_all.columns.tolist().index('group')
        group = 1
        dist = int(df_all.shape[0] / groups)
        for j in range(0, df_all.shape[0], dist):
            if group < groups:
                df_all.iloc[j: j + dist, group_index] = group
            else:
                df_all.iloc[j:, group_index] = group
                break
            group += 1
        df_group = df_all.groupby(['group']).apply(lambda x: sum(x.return_rate * (x.close_now / x.close_now.sum()))).to_frame()
        df_group = df_group.rename(columns={0: 'return_rate'})
        df_group = df_group.transpose()
        new_names = ['group{:0>2}'.format(i) for i in range(1, groups + 1)]
        df_group.columns = new_names
        df_group['date'] = date_now
        df_daily = df_daily.append(df_group)
    df_daily = df_daily.reset_index().drop(['index'], 1)
    df_daily['diff'] = df_daily['group{:0>2}'.format(groups)] - df_daily['group01']
    if save_daily:
        df_daily.to_csv(os.path.join(PROJECT_FILES_PATH, 'daily_return', "{}_cycle_{}_daily.csv".format(index_std, cycle)), index=False, encoding='utf-8')
    df_cum = df_daily.copy()
    for i in range(df_daily.shape[0]):
        if i == 0:
            df_cum.iloc[i, 0:groups] = 1
        else:  # 单利计算累计收益
            df_cum.iloc[i, 0:groups] = df_cum.iloc[i - 1, 0:groups] + df_daily.iloc[i - 1, 0:groups]
    if save_cum:
        df_cum.to_csv(os.path.join(PROJECT_FILES_PATH, 'cum_return', "{}_cycle_{}_cum.csv".format(index_std, cycle)), index=False, encoding='utf-8')
    fig = plt.figure(figsize=(12, 6))
    plt.ylabel("单利累计收益")
    ax = plt.subplot(111)
    df_cum = df_cum.set_index('date')
    df_cum[['group01', 'group{:0>2}'.format(groups)]].plot(ax=ax)
    ax.set_title("{}单利累计收益图  cycle={}".format(index_std, cycle))
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    if save_plot:
        picfile = os.path.join(PROJECT_FILES_PATH, 'plot', "{}_cycle_{}_cum.png".format(index_std, cycle))
        plt.savefig(picfile)
        print("plot is saved to: {}".format(picfile))


def get_ttest_result_for_index_std_on_given_folder(start_date, end_date, folder_path):
    """
    在给定时间段内对index_std文件夹下的所有index_std return进行配对t检验并返回字典 然后按p值升序排列 越靠前越有效
    """

    result = {}
    file_names = listdir_advanced(folder_path, "csv", strip=False)
    names = ['_'.join(ins.split('_')[:-4]) for ins in file_names]
    for index, file in enumerate(file_names):
        df = pd.read_csv(os.path.join(folder_path, file))
        df = df[df.date.between(start_date, end_date)]
        df = df[['group01', 'group10']]
        result[names[index]] = {'pvalue': paired_ttest(df)[1], 'ascending': np.nan}
        if df.group01.sum() > df.group10.sum():  # 最小组的收益大于最大组收益 即说明越小越好，所以选择升序排名 越小的指标排名越靠前
            result[names[index]]['ascending'] = 1
        else:
            result[names[index]]['ascending'] = 0
    result = {key + '_std': result[key] for key in result}
    return result


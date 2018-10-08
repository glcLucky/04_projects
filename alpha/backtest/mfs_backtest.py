# -*- coding: utf-8 -*-

"""
mfs_backtest.py
多因子选股模型回测框架

@author: Gui lichao
@date: 2018-04-20

"""

import pandas as pd
import numpy as np
import os

import finkit.api as fk
import devkit.api as dk
import matplotlib.pyplot as plt
import DataAPI
from .. config import DB_PATH


def derive_next_month_rr(sec_ids, start_date, end_date):
    """
    获取给定股票列表在给定日期列表的下个月收益率
    @sec_ids <list>: 股票列表
    @start_date <"%Y-%m-%d">: 开始日期
    @end_date <"%Y-%m-%d">: 结束日期
    @return dataframe [sec_id yearmonth month_ret CLOSE]
    """
    # 取月初月末的交易日列表
    tds = dk.json2dict(os.path.join(DB_PATH, r"datasets\pre\trading_days.json"))
    tds = pd.DataFrame(tds, columns=['date'])
    tds = tds[tds.date.between(start_date, end_date)]
    tds['group'] = tds['date'].apply(lambda x: x[:7])
    tds = tds.sort_values(['date'])
    first = tds.groupby('group').head(1)
    last = tds.groupby('group').tail(1)
    tds = first.append(last)
    tds = tds.sort_values('date')
    # 获取月初月末交易日的收盘价
    close = DataAPI.api.get_secs_indicator_on_multidays(indicator="CLOSE", trading_days=tds.date.tolist(), sec_ids=sec_ids)
    close = close.sort_values(['sec_id', 'date'])
    close['yearmonth'] = close['date'].apply(lambda x: x[:7])
    # 获取月收益率
    def cal_ret(x):
        close_id = x.columns.tolist().index('CLOSE')
        return x.iloc[-1, close_id] / x.iloc[0, close_id] - 1
    df_target = close.groupby(['sec_id', 'yearmonth'], as_index=False).apply(lambda x: cal_ret(x))
    df_target = df_target.reset_index().rename(columns={0: 'month_ret'})
    # 只取每个月月初的收盘价
    close = close.groupby(['sec_id', 'yearmonth'], as_index=False).apply(lambda x: x.head(1))
    df_target = df_target.merge(close, how='inner', on=['sec_id', 'yearmonth'])
    del df_target['date']
    return df_target


def backtest_for_mfs(yearmonth, selected_sec_ids, benchmark, model_name, label_kind="label_A", override=False):
    """
    多因子选股回测框架
    @yearmonth <"%Y-%m">: 年份和月份
    @selected_sec_ids <list>: yearmonth: selected sec_ids
    @benchmark <str>: 基准收益 目前支持 hs300 zz500 wind_ALL_A
    @plot <bool>: 是否绘制累计收益图
    @model_name <str>: 模型名称
    @label_kind <str>: 标记获得方法
    """
    back_test_path = os.path.join(DB_PATH, r"backtest\{}\{}\{}".format(model_name, label_kind, benchmark))
    file_path = os.path.join(back_test_path, "records_{}.json".format(yearmonth))
    # yearmonth =
    if not os.path.exists(back_test_path):
        os.makedirs(back_test_path)

    if os.path.exists(file_path) and (not override):
        return
    records = {}
    # 获取所有各月度的收益率和月初股价
    df_rr_monthly = pd.read_csv(os.path.join(DB_PATH, r"datasets\pre\rr_monthly.csv"))
    df_rr_monthly_1 = df_rr_monthly.set_index(['sec_id', 'yearmonth'])
    df_rr_monthly_1 = df_rr_monthly_1.sort_index(level='sec_id')
    perform = df_rr_monthly_1.loc[(selected_sec_ids, yearmonth), ['CLOSE', 'month_ret']]
    model_ret = (perform['CLOSE'] * perform['month_ret']).sum() / perform['CLOSE'].sum()
    benchmark_rr = df_rr_monthly[df_rr_monthly['sec_id'] == benchmark]
    benchmark_rr = benchmark_rr.set_index(['yearmonth'])
    benchmark_ret = benchmark_rr.loc[yearmonth, 'month_ret']
    records[yearmonth] = {"model": model_ret, "benchmark": benchmark_ret, "selected_sec_ids": ",".join(selected_sec_ids)}
    dk.dict2json(records, file_path)
    # records[yearmonth] = {"return": (perform['CLOSE'] * perform['month_ret']).sum() / perform['CLOSE'].sum(), "selected_stocks": selected}
    # for yearmonth in list(selected_sec_ids.keys()):
    #     selected = selected_sec_ids[yearmonth]
    #     # 获得入选股票在下个月的收益率
    #     perform = benchmark_rr_monthly.loc[(selected, yearmonth), ['CLOSE', 'month_ret']]
    # records[yearmonth] = {"return": (perform['CLOSE'] * perform['month_ret']).sum() / perform['CLOSE'].sum(), "selected_stocks": selected}

    # df_records = pd.DataFrame([[i, v['return'], v['selected_stocks']] for i, v in records.items()], columns=['yearmonth', 'month_ret', 'selected_stocks'])
    # df_records = df_records.rename(columns={'month_ret': 'model_ret'})
    # 获取基准收益
    # benchmark_rr = pd.read_csv(os.path.join(DB_PATH, r"datasets\return_rate\{}_index_rr_monthly.csv".format(benchmark)))
    # benchmark_rr = benchmark_rr.set_index(['yearmonth'])
    # benchmark_rr = benchmark_rr.rename(columns={'month_ret': 'benchmark_rr'})
    # del benchmark_rr['CLOSE']
    # del benchmark_rr['sec_id']
    # benchmark_ret = benchmark_rr.loc[yearmonth, 'month_ret']
    # records[yearmonth] = {"model": model_ret, "benchmark": benchmark_ret, "selected_sec_ids": ",".join(selected_sec_ids)}
    # dk.dict2json(records, file_path)
    # df_records = df_records.merge(benchmark_rr, how='left', on=['yearmonth'])
    # df_records.to_csv(os.path.join(back_test_path, "df_records_{}".format(yearmonth))

    # df_records_daily = df_records.copy()
    # # 获取模型和基准累计净值
    # for ix in df_records.index:
    #     if ix == 0:
    #         df_records.loc[ix, 'model_ret_cum'] = 1
    #         df_records.loc[ix, 'benchmark_rr_cum'] = 1
    #     else:
    #         df_records.loc[ix, 'model_ret_cum'] = df_records.loc[ix - 1, 'model_ret_cum'] * (1 + df_records.loc[ix, 'model_ret'])
    #         df_records.loc[ix, 'benchmark_rr_cum'] = df_records.loc[ix - 1, 'benchmark_rr_cum'] * (1 + df_records.loc[ix, 'benchmark_rr'])
    # df_records = df_records[['yearmonth', 'benchmark_rr_cum', 'model_ret_cum']].set_index('yearmonth')
    # df_records .to_csv(os.path.join(back_test_path, "df_records_{}.csv".format(dataID)))
    # if plot:
    #     fig, ax = plt.subplots()
    #     fig.set_size_inches(20, 10)
    #     ax.plot(df_records)
    #     ax.legend(df_records.columns, fontsize=22)
    #     plt.title("基于测试集{}选股累计收益与沪深300累计净值比较图 {}--{}".format(model_name, min(list(selected_sec_ids.keys())), max(list(selected_sec_ids.keys()))), fontsize=22)
    #     plt.xlabel("日期", fontsize=22)
    #     plt.ylabel("累计净值", fontsize=22)
    #     plt.savefig(os.path.join(back_test_path, "LJJZ_{}.png".format(dataID)))

    # 计算回测指标
    # 年化收益率
    # rr_annually = (df_records.iloc[-1, :] - df_records.iloc[0, :]) / df_records.iloc[0, :]

    # 夏普比率
    # risk_free_int = dk.json2dict(os.path.join(DB_PATH, r"datasets\pre\risk_free_int.json"))

    # sharp_ratio = {}
    # sharp_ratio['model'] = (rr_annually['model_ret_cum'] - risk_free_int[ID2DATE[str(dataID)]['TEST'][0][:4]]) / np.std(df_records_daily['model_ret'])
    # sharp_ratio['benchmark'] = (rr_annually['benchmark_rr_cum'] - risk_free_int[ID2DATE[str(dataID)]['TEST'][0][:4]]) / np.std(df_records_daily['benchmark_rr'])

    # 最大回撤
    # max_back = {}
    # col_names = df_records.columns.tolist()
    # for i in range(df_records.shape[0]):
    #     for j in range(df_records.shape[1]):
    #         if i > 0:
    #             back = np.max(df_records.iloc[:i, j]) / df_records.iloc[i, j] - 1
    #             if back > 0:  # 当前净值小于历史最大值：
    #                 if back > max_back[col_names[j]]:
    #                     max_back[col_names[j]] = back
    #         else:
    #             max_back[col_names[j]] = 0

    # alpha = df_records.iloc[-1, 1] - df_records.iloc[-1, 0]
    # info_ratio = (df_records_daily['model_ret'] - df_records_daily['benchmark_rr']).mean() / (df_records_daily['model_ret'] - df_records_daily['benchmark_rr']).std()

    # a1 = rr_annually.to_frame().T.rename(columns={"benchmark_rr_cum": "benchmark", "model_ret_cum": "model"})
    # a1['index'] = "年化收益率"
    # a2 = pd.DataFrame([[k, v] for k, v in max_back.items()]).set_index(0).T.rename(columns={"benchmark_rr_cum": "benchmark", "model_ret_cum": "model"})
    # a2['index'] = "最大回撤率"
    # # a3 = pd.DataFrame([[k, v] for k, v in sharp_ratio.items()]).set_index(0).T
    # # a3['index'] = "夏普比率"
    # df_metrics = a1.append(a2)
    # df_metrics = df_metrics.append(pd.Series({'benchmark': 0, 'model': info_ratio, 'index': "信息比率"}), ignore_index=True)
    # df_metrics = df_metrics.append(pd.Series({'benchmark': 0, 'model': alpha, 'index': "超额收益率"}), ignore_index=True)
    # df_metrics['period'] = "{}--{}".format(min(list(selected_sec_ids.keys())), max(list(selected_sec_ids.keys())))
    # df_metrics = df_metrics.reindex(columns=[['period', 'index', 'benchmark', 'model']])
    # df_metrics.to_csv(os.path.join(back_test_path, "history_backtest_metrics_{}.csv".format(dataID)), index=0)
    # print(df_metrics)


def plot_LLJZ(yearmonth_st, yearmonth_end, model_name="XGBoost", label_kind="label_A", benchmark="hs300"):
    file_root = os.path.join(DB_PATH, "backtest", model_name, label_kind, benchmark)
    file_LJJZ = os.path.join(file_root, "LLJZ", "{}--{}".format(yearmonth_st, yearmonth_end))
    if not os.path.exists(file_LJJZ):
        os.makedirs(file_LJJZ)
    year_st_num = int(yearmonth_st[:4])
    year_end_num = int(yearmonth_end[:4])
    diff = year_end_num - year_st_num
    yearmonth_lst = [str(year_st_num + i) + '-{:0>2}'.format(str(1 + j)) for i in range(0, diff + 1) for j in range(0, 12)]
    yearmonth_lst = [yearmonth for yearmonth in yearmonth_lst if (yearmonth >= yearmonth_st) & (yearmonth <= yearmonth_end)]
    records = {}
    for yearmonth in yearmonth_lst:
        records.update(dk.json2dict(os.path.join(file_root, "records_{}.json".format(yearmonth))))
    date_st = dk.date2char(dk.char2datetime(yearmonth_st + '-31') - dk.timedelta({'months': 1}))
    records[date_st] = {'benchmark': 1, 'model': 1}
    df_records = pd.DataFrame(records).T.reset_index().rename(columns={'index': 'yearmonth'})

    df_records.to_csv(os.path.join(file_LJJZ, "df_records.csv"), index=0)

    df_records_daily = df_records[['yearmonth', 'benchmark', 'model']]
    # 获取模型和基准累计净值
    for ix in df_records_daily.index:
        if ix == 0:
            df_records_daily.loc[ix, 'model_rr_cum'] = 1
            df_records_daily.loc[ix, 'benchmark_rr_cum'] = 1
        else:
            df_records_daily.loc[ix, 'model_rr_cum'] = df_records_daily.loc[ix - 1, 'model_rr_cum'] * (1 + df_records_daily.loc[ix, 'model'])
            df_records_daily.loc[ix, 'benchmark_rr_cum'] = df_records_daily.loc[ix - 1, 'benchmark_rr_cum'] * (1 + df_records_daily.loc[ix, 'benchmark'])
    df_records_daily = df_records_daily[['yearmonth', 'benchmark_rr_cum', 'model_rr_cum']].set_index('yearmonth')
    # df_records_daily .to_csv(os.path.join(back_test_path, "df_records_daily_{}.csv".format(dataID)))
    fig, ax = plt.subplots()
    fig.set_size_inches(20, 10)
    ax.plot(df_records_daily)
    ax.legend(df_records_daily.columns, fontsize=22)
    plt.title("基于测试集{}选股累计收益与{}累计净值比较图 {}--{}".format(model_name, benchmark, yearmonth_st, yearmonth_end), fontsize=22)
    plt.xlabel("日期", fontsize=22)
    plt.ylabel("累计净值", fontsize=22)
    plt.savefig(os.path.join(file_LJJZ, "LJJZ.png"))

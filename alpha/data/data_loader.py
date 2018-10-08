# -*- coding: utf-8 -*-

"""
data_loader.py

数据加载器
"""
import os
import pandas as pd
import pickle
import numpy as np
import DataAPI
import devkit.api as dk
from functools import partial

from . tools import (
    derive_label_A,
    derive_label_B,
)
from .. config import DB_PATH
from .. backtest import derive_next_month_rr
from . preprocessing import (
    wash_train_data,
    wash_test_data,
)
label_kind_funcs = {
    "label_A": partial(derive_label_A, lp=0.3, up=0.7),
    "label_B": derive_label_B,
}


def get_monthly_feats_on_given_period(start_date, end_date, stock_pool=[], inds_ts=[], inds_fr=[], LP=0.05, UP=0.95, NEW_CP=100):
    """
    获得指定区间内指定特征的月度数据
    @start_date<"%Y-%m-%d">: 开始日期
    @end_date<"%Y-%m-%d">: 结束日期
    @stock_pool <list>: 股票池列表 默认为为空 表示全A股
    @ind_ts <list>: 时间序列指标列表 默认为空 表示所有可行
    @ind_fr <list>: 财报数据列表 默认为空 表示所有可行
    @LP <int>: 流通市值上分位数 流通市值介于LP与UP之间
    @UP <int>: 流通市值下分位数
    @NEC_CP <int>: 次新股的定义 默认为100 表示上市日期小于100的为次新股 将会被剔除
    """
    sec_ids = stock_pool
    trading_days = DataAPI.api.get_monthly_last_trading_days(start=start_date, end=end_date)

    # 获取满足条件的所有股票
    df_size = DataAPI.read.get_secs_indicator_on_multidays(indicator='MKT_CAP_FLOAT', sec_ids=sec_ids, trading_days=trading_days)
    df_ipo_listdays = DataAPI.read.get_secs_indicator_on_multidays(indicator='IPO_LISTDAYS', sec_ids=sec_ids, trading_days=trading_days)
    df_low = DataAPI.read.get_secs_indicator_on_multidays(indicator='LOW', sec_ids=sec_ids, trading_days=trading_days)
    df_high = DataAPI.read.get_secs_indicator_on_multidays(indicator='HIGH', sec_ids=sec_ids, trading_days=trading_days)
    df_pe = DataAPI.read.get_secs_indicator_on_multidays(indicator='VAL_PE_DEDUCTED_TTM', sec_ids=sec_ids, trading_days=trading_days)

    df_sec_ids = df_size.merge(df_ipo_listdays, how='inner', on=['sec_id', 'date'])
    df_sec_ids = df_sec_ids.merge(df_low, how='inner', on=['sec_id', 'date'])
    df_sec_ids = df_sec_ids.merge(df_high, how='inner', on=['sec_id', 'date'])
    df_sec_ids = df_sec_ids.merge(df_pe, how='inner', on=['sec_id', 'date'])

    df_sec_ids = df_sec_ids[df_sec_ids.VAL_PE_DEDUCTED_TTM > 0]  # 剔除亏损股票
    df_sec_ids = df_sec_ids[df_sec_ids.HIGH != df_sec_ids.LOW]  # 剔除停牌股
    df_sec_ids = df_sec_ids[df_sec_ids.IPO_LISTDAYS >= NEW_CP]  # 剔除次新股

    a = df_sec_ids.groupby(['date']).MKT_CAP_FLOAT.quantile(LP).to_frame().reset_index().rename(columns={'MKT_CAP_FLOAT': "size_LP"})
    df_sec_ids = df_sec_ids.merge(a, how='inner', on=['date'])
    a = df_sec_ids.groupby(['date']).MKT_CAP_FLOAT.quantile(UP).to_frame().reset_index().rename(columns={'MKT_CAP_FLOAT': "size_UP"})
    df_sec_ids = df_sec_ids.merge(a, how='inner', on=['date'])

    df_sec_ids = df_sec_ids[df_sec_ids.MKT_CAP_FLOAT.between(df_sec_ids['size_LP'], df_sec_ids['size_UP'])]

    sec_ids = {}
    date_list = list(set(df_sec_ids['date']))
    for date in date_list:
        sec_ids[date] = list(df_sec_ids[df_sec_ids['date'] == date]['sec_id'])

    if (len(inds_ts) == 0) and (len(inds_fr) == 0):
        # 获取所有可行的特征列表
        schema = pd.DataFrame(DataAPI.schema.get_schema("indicator")).T
        schema = schema[~schema.aspect.isin(['辅助指标', '价量指标'])]
        inds_fr = schema[schema.type == '财报数据'].index.tolist()
        inds_ts = schema[schema.type == '时间序列'].index.tolist()
        # 这几个特征暂时没取完 为了避免下面的读写错误 先删除这个变量
        inds_ts.remove('TECH_CRY')
        inds_ts.remove('TECH_MAWVAD')
        inds_ts.remove('TECH_PSY')
        inds_ts.remove('TECH_REVS10')
        inds_ts.remove('TECH_REVS120')
        inds_ts.remove('TECH_REVS20INDU1')
        inds_ts.remove('TECH_REVS250')
        inds_ts.remove('TECH_REVS5')
        inds_ts.remove('TECH_REVS5INDU1')
        inds_ts.remove('TECH_REVS60')
        inds_ts.remove('TECH_REVS750')
        inds_ts.remove('TECH_TURNOVERRATE120')
        inds_ts.remove('TECH_TURNOVERRATE240')
        inds_ts.remove('TECH_TURNOVERRATE5')
        inds_ts.remove("TECH_TURNOVERRATE60")
        inds_ts.remove("TECH_TURNOVERRATE20")

    # 获得时间序列指标
    df_inds = pd.DataFrame()
    for ind in inds_ts:
        df_ind = pd.DataFrame()
        for date in trading_days:
            a = DataAPI.read.get_secs_indicator(indicator=ind, sec_ids=sec_ids[date], date=date).reset_index()
            a['date'] = date
            df_ind = df_ind.append(a)
        if len(df_inds) == 0:
            df_inds = df_ind.copy()
        else:
            df_inds = df_inds.merge(df_ind, how='outer', on=['sec_id', 'date'])

    # 财务报表指标
    df_inds['date_available'] = df_inds['date'].apply(lambda x: dk.get_available_report_day(x))
    report_days_to_load = list(set(df_inds['date_available']))
    secs_list_temp = list(set(df_inds['sec_id']))  # 由于财报数据取报告日 为了保证所有需要股票都取到 取时间序列指标各月末入选股票的并集
    df_frs = pd.DataFrame()
    for ind in inds_fr:
        df_fr = pd.DataFrame()
        for date in report_days_to_load:
            a = DataAPI.read.get_secs_indicator(indicator=ind, sec_ids=secs_list_temp, date=date).reset_index()
            a['date'] = date
            df_fr = df_fr.append(a)
        if len(df_frs) == 0:
            df_frs = df_fr.copy()
        else:
            df_frs = df_frs.merge(df_fr, how='outer', on=['sec_id', 'date'])
    df_frs = df_frs.rename(columns={'date': 'date_available'})
    df_inds = df_inds.merge(df_frs, how='left', on=['sec_id', 'date_available'])
    return df_inds


def get_analysis_data(date_list, dataID, type, label_kind="label_A", override=False):
    """
    获得脏的数据集 主要包括获得区间内的特征，计算标记
    @date_list<["%Y-%m-%d"]>: 日期列表
    @type <'str'>: 数据集类型 训练集 or测试集
    @label_kind <str>: 计算标记类型
    """
    date_list = sorted(date_list)
    dataID = date_list[0][:7]
    root_path = os.path.join(DB_PATH, r"datasets\{}_dirty\{}".format(type, label_kind))
    if not os.path.exists(root_path):
        os.makedirs(root_path)
    dirty_path = os.path.join(DB_PATH, root_path, r"df_{}_{}.csv".format(type, dataID))
    if os.path.exists(dirty_path) and (not override):
        print("该{}的脏数据已存在，无需计算，直接读入".format(type))
        df_dirty = pd.read_csv(dirty_path)
        return df_dirty

    # 从特征库中获得特征
    df_feats = pd.DataFrame()
    for date in date_list:
        a = pd.read_csv(os.path.join(DB_PATH, r"datasets\raw_indicators_by_month\{}.csv".format(date[:7])))
        df_feats = df_feats.append(a)
    df_feats['yearmonth'] = df_feats['date'].apply(lambda x: dk.date2char(dk.char2datetime(x) + dk.timedelta({'months': 1}))[:7])
    st = df_feats['yearmonth'].min() + '-01'
    end = df_feats['yearmonth'].max() + '-31'
    if type == 'train':
        df_return = derive_next_month_rr(list(set(df_feats['sec_id'])), st, end)
        df_raw = df_feats.merge(df_return, how='inner', on=['sec_id', 'yearmonth'])
        yearmonth = sorted(list(set(df_raw.yearmonth)))
        group_id = pd.DataFrame(yearmonth, columns=['yearmonth'], index=range(1, len(yearmonth) + 1))
        group_id = group_id.sort_values(['yearmonth'])
        group_id = group_id.reset_index().rename(columns={'index': 'group_id'})
        df_raw = df_raw.merge(group_id, how='left', on=['yearmonth'])
        df_dirty = label_kind_funcs[label_kind](df_raw)
    else:
        df_dirty = df_feats
    df_dirty.to_csv(dirty_path, index=0)
    return df_dirty


def preprocess_train_data(df_train_dirty, dataID, overmissing_th=0.1, label_kind="label_A", override=False):
    """
    对脏的训练集进行清洗 包括删除过多的特征 缺失值处理 特殊变量的转换 统计标准换 异常样本处理
    @df_train_dirty <dataframe>: 脏的数据集
    @overmissing_th <flo>: 过度缺失而要删除特征的
    @DATAID <"%Y-%m-%d">: 训练集编号
    @label_kind <str>: 标记获得类型 目前有A和B两种 默认为A
    """
    # 删除缺失过多的特征 然后删除缺失样本
    root_path = os.path.join(DB_PATH, r"datasets\train_clean\{}".format(label_kind))
    if not os.path.exists(root_path):
        os.makedirs(root_path)
    clean_path = os.path.join(DB_PATH, root_path, "df_train_{}.csv".format(dataID))
    if os.path.exists(clean_path) and (not override):
        print("该训练期的干净数据已存在，无需计算，直接读入")
        df_train_clean = pd.read_csv(clean_path)
        return df_train_clean

    def drop_overmissing_feats(dsi, threshold):
        """
        删除缺失过多的特征  然后剔除有缺失值的样本
        """
        a = dsi.isnull().sum() / len(dsi) < threshold
        feats_to_retain = a[a].index
        dsi = dsi[feats_to_retain].dropna()
        dsi = dsi.reset_index()
        del dsi['index']
        return dsi
    df_train_dirty = drop_overmissing_feats(df_train_dirty, overmissing_th)

    # 特殊变量转换
    # 将估值类指标取倒数
    df_train_dirty['VAL_PE_DEDUCTED_TTM'] = 1 / df_train_dirty['VAL_PE_DEDUCTED_TTM']
    df_train_dirty['PS_TTM'] = 1 / df_train_dirty['PS_TTM']
    df_train_dirty['PCF_OCF_TTM'] = 1 / df_train_dirty['PCF_OCF_TTM']
    df_train_dirty['PB_LF'] = 1 / df_train_dirty['PB_LF']
    # 流通市值取对数
    df_train_dirty['MKT_CAP_FLOAT'] = np.log(df_train_dirty['MKT_CAP_FLOAT'])

    # 删除无用特征
    droplist = ['sec_id', 'yearmonth', 'month_ret', 'group_id', 'CLOSE', 'date', 'date_available']
    df_train_dirty = df_train_dirty.drop(droplist, axis=1)

    # 统计标准化
    std_root_path = os.path.join(DB_PATH, r"datasets\train_dirty\std_info")
    if not os.path.exists(std_root_path):
        os.makedirs(std_root_path)
    std_path = os.path.join(std_root_path, "std_info_{}.txt".format(dataID))
    if not os.path.exists(std_path) or override:
        # 将训练集样本均值和标准差存入文件以便测试集使用
        train_mean = df_train_dirty.iloc[:, :-1].mean()
        train_std = df_train_dirty.iloc[:, :-1].std()
        f = open(std_path, 'wb')
        std_info = {"mean": train_mean, "std": train_std}
        pickle.dump(std_info, f, 0)
        f.close()
    else:
        f = open(std_path, 'rb')
        std_info = pickle.load(f)
        f.close()
    df_train_dirty.iloc[:, :-1] = (df_train_dirty.iloc[:, :- 1] - std_info['mean']) / std_info['std']
    # 其他预处理 包括极端值 极端样本 特征筛选等等 待完善

    # 将清洗后的数据存入本地文件
    df_train_dirty.to_csv(clean_path, index=0)
    return df_train_dirty


def preprocess_test_data(df_test_dirty, dataID, keep_vars, label_kind="label_A", override=False):
    """
    对脏的测试集进行清洗 包括删除过多的特征 缺失值处理 特殊变量的转换 统计标准换 异常样本处理
    @df_test_dirty <dataframe>: 脏的数据集
    @keep_vars <list>: 需要保留的变量 仅保留和训练集一致的变量 对于测试集不能删除特征 因为会导致与训练的模型特征不一致 只能删除缺失的样本
    @DATAID <"%Y-%m-%d">: 训练集编号
    @label_kind <str>: 标记获得类型 目前有A和B两种 默认为A
    """
    # 删除缺失过多的特征 然后删除缺失样本
    root_path = os.path.join(DB_PATH, r"datasets\test_clean\{}".format(label_kind))
    clean_path = os.path.join(DB_PATH, root_path, r"df_test_{}.csv".format(dataID))
    if not os.path.exists(root_path):
        os.makedirs(root_path)
    if os.path.exists(clean_path) and (not override):
        print("该测试期的干净数据已存在，无需计算，直接读入")
        df_test_clean = pd.read_csv(clean_path)
        df_test_clean = df_test_clean.set_index(['sec_id', 'date'])
        return df_test_clean

    df_test_dirty = df_test_dirty.set_index(['sec_id', 'date'])
    # df_test_dirty = df_test_dirty[keep_vars].dropna(axis=1)
    df_test_dirty = df_test_dirty.reindex(columns=keep_vars)  # 确保训练集和测试集变量顺序一致
    # 特殊变量转换
    # 将估值类指标取倒数
    df_test_dirty['VAL_PE_DEDUCTED_TTM'] = 1 / df_test_dirty['VAL_PE_DEDUCTED_TTM']
    df_test_dirty['PS_TTM'] = 1 / df_test_dirty['PS_TTM']
    df_test_dirty['PCF_OCF_TTM'] = 1 / df_test_dirty['PCF_OCF_TTM']
    df_test_dirty['PB_LF'] = 1 / df_test_dirty['PB_LF']
    # 流通市值取对数
    df_test_dirty['MKT_CAP_FLOAT'] = np.log(df_test_dirty['MKT_CAP_FLOAT'])

    # 统计标准化

    std_root_path = os.path.join(DB_PATH, r"datasets\train_dirty\std_info")
    std_path = os.path.join(std_root_path, "std_info_{}.txt".format(dataID))

    if not os.path.exists(std_path):
        dk.Logger.warning("对应训练集标准化数据不存在，请先更新对应训练集")
        return
    else:
        f = open(std_path, 'rb')
        std_info = pickle.load(f)
        f.close()
    df_test_dirty.iloc[:, :-1] = (df_test_dirty.iloc[:, :- 1] - std_info['mean']) / std_info['std']
    # 其他预处理 包括极端值 极端样本 特征筛选等等 待完善
    # 将清洗后的数据存入本地文件
    df_test_dirty.to_csv(clean_path)
    return df_test_dirty

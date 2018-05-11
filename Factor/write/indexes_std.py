# -*- coding: utf-8 -*-

"""
indexes_std.py

对原始指标进行处理
包括统计标准化、异常值检测、缺失值处理等。

方法如下：
1. 缺失值处理: 直接删除index为空的股票
2. 统计标准化: 对每一天全部备选股计算均值方差，然后进行标准化
3. 异常值处理: 直接删除在3倍标准差之外的样本
@author: Gui lichao
@date: 2018.04.08

-------------------

"""
import gc
from devkit.api import Logger, df2mysql

from .. utils import process_ts_index, get_unique_datelist_from_table
from .. config import (USER, PASSWORD)
from .. read import get_secs_index


def update_index(index, path, log=False, IsReport=False):
    """
    根据csv文件写入index到MySQL数据库
    @index <str>: index名称
    @path <str>: csv文件路径 格式 对于市场数据: date sec_id index名称 对于财报数据: date_report 指标名称
    @IsReport <str>: 周期是否是report date 对于财务数据是true
    """
    df = pd.read_csv(path, encoding='utf-8')
    df = df.dropna(how='any')
    if IsReport:
        dummy = get_secs_index('dummy')
        df = df.rename(columns={'date_report': 'date_report_available'})
        df = dummy.merge(df, how='inner', on=['sec_id', 'date_report_available'])
    return df


def update_index_std(index, cp=3, log=False):
    """
    更新index_std
    更新原理: 无需指定trading_days 更新全部index中有的日期但在index_std中没有的日期
    @index <str>: index名称 不是index_std名称
    @cp <int>: winsorize的临界值
    """

    trading_days = get_unique_datelist_from_table("index", index)
    existed_days = get_unique_datelist_from_table("index_std", "{}_std".format(index))
    update_days = sorted(list(set(trading_days) - set(existed_days)))
    if len(update_days) == 0:
        Logger.warn("All given dates has existed. No need to update!!")
        return
    output = process_ts_index(index, update_days, cp)
    if len(output) == 0:
        Logger.error("Fail to process {} on given dates".format(index))
    df2mysql(USER, PASSWORD, "index_std", index + '_std', output)
    del output, trading_days, update_days
    gc.collect()
    Logger.info("Updated successfully!!")

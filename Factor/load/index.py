# -*- coding: utf-8 -*-

"""
index.py
获取index

"""
import pandas as pd
from .. read import get_secs_IC


def processing_index(index, trading_days, cp=3):
    """
    给定trading_days列表，处理原始指标 包括剔除当天停牌股、st股，统计标准化，剔除cp倍标准差之外的样本
    @index <str>: 指标名称
    @trading_days <list>: 交易日列表
    @cp <float>: critical point 极端值处理的阈值  默认为3
    """

    output = pd.DataFrame()
    df_ic = get_secs_IC(ic_code='stocks_info', trading_days=trading_days)
    for date in trading_days:
        temp = pd.DataFrame()
        df_ic1 = df_ic[df_ic.date == date]
        conds = (df_ic1.is_trade == 1).multiply(df_ic1.is_st == 0)
        df_ic2 = df_ic1[conds]
        sec_ids = df_ic2.sec_id.tolist()
        temp1 = factor.read.get_secs_index_on_multidays(index, sec_ids, [date])
        if len(temp1) != 0:
            temp1[index] = (temp1[index] - temp1[index].mean()) / temp1[index].std()  # 统计标准化
            temp2 = temp1[temp1.vol_5days.abs() <= cp]  # 删除极端值
            output = output.append(temp2)
        else:
            continue
    return output

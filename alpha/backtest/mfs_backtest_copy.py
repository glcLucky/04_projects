# -*- coding: utf-8 -*-

"""
mfs_backtest.py
多因子选股模型回测框架

@author: Gui lichao
@date: 2018-04-20

"""

import pandas as pd
import numpy as np
from Factor.read import (
    get_secs_index,
)
import finkit.api as fk
import devkit.api as dk


def calculate_period_return(start, end, sec_id=[], price_type='close'):
    """
    @sec_id <list>: 股票列表
    @price_type <str>: 价格类型 close open high low
    """
    a = get_secs_index(index=price_type, sec_ids=sec_id, trading_days=[start])
    a = a[['sec_id', price_type]].rename(columns={price_type: price_type + '_start'})
    b = get_secs_index(index=price_type, sec_ids=sec_id, trading_days=[end])
    b = b[['sec_id', price_type]].rename(columns={price_type: price_type + '_end'})
    c = a.merge(b, on=['sec_id'])
    d = c['{}_end'.format(price_type)].sum() / c['{}_start'.format(price_type)].sum() - 1
    return d


def stop_loss_or_profit(sec_ids, start_date, end_date, stoploss, stopprofit, price_type='close', log=False):
    """
    在给定的有序交易日内第一天持仓给定股票 持有期间内 当损失或盈利大于阈值时卖出 到期间最后一天时 无论是否达到阈值全部清仓 获得此种策略下的综合收益率
    @sec_id <list>: 股票代码列表
    @start_date <'%Y-%m-%d'>: 开始日期
    @end_date <'%Y-%m-%d'>: 结束日期
    @stoploss <float>: 止损率 如=-0.1 即当浮亏率达到10%时卖出
    @stopprofit <float>: 止盈率 如=0.1 即当浮盈率达到10%时卖出
    @price_type <str>: 使用的价格类型 默认为收盘价
    """
    trading_days = fk.get_trading_days(start_date, end_date)
    trading_days = sorted(trading_days)
    close = get_secs_index(price_type, sec_ids, trading_days)  # 获取收盘价信息
    date_open = trading_days[0]  # 建仓日
    date_close = trading_days[-1]  # 强制平仓日
    cost_info = close[close.date == date_open]  # 建仓日成本信息
    cost_info = cost_info.rename(columns={price_type: '{}_buy'.format(price_type)})
    cost_info = cost_info.set_index('sec_id')
    records = cost_info.copy()  # 存储持仓股票买卖价格
    records['{}_sell'.format(price_type)] = np.nan
    records['date_sell'] = np.nan
    close_new = pd.DataFrame()

    for date in trading_days[1:]:
        now = close[close.date == date]
        now = now.set_index('sec_id')
        if date == date_close:
            stocks_hold_to_maturity = records[records.close_sell.isnull()].index.tolist()
            # 获取在强制平仓日仍持仓的股票列表
            existed_sec_ids = now.index.tolist()
            # 对于那些在强制平仓日停牌的持仓股票 暂时不处理 直接丢掉
            stocks_hold_to_maturity = list(set(stocks_hold_to_maturity).intersection(existed_sec_ids))
            sellstocks = now.loc[stocks_hold_to_maturity]
            sellstocks = sellstocks.rename(columns={price_type: '{}_sell'.format(price_type)})
            sellstocks['date_sell'] = date
            records.update(sellstocks)
            continue
        else:
            # 获取截至今日的浮动盈亏率
            now = now.rename(columns={price_type: '{}_now'.format(price_type)})
            del now['date']
            close_all = cost_info.merge(now, how='left', left_index=True, right_index=True)
            close_all['ret_rate'] = close_all['{}_now'.format(price_type)] / close_all['{}_buy'.format(price_type)] - 1
            close_all = close_all.replace(np.nan, 0)
            # 对于那些当日未取得股价的股票设置收益率为0 这样既不会被止损卖出也不会被止盈卖出
            # 计算止损卖出的股票并存入records
            sellstocks = close_all[close_all.ret_rate < stoploss]
            if len(sellstocks) != 0:
                if log:
                    dk.Logger.info("以下股票由于亏损大于{}被强制卖出: {}".format(stoploss, sellstocks.index.tolist()))
                sellstocks = sellstocks.rename(columns={'{}_now'.format(price_type): '{}_sell'.format(price_type)})
                sellstocks['date_sell'] = date
                del sellstocks['close_buy']
                records.update(sellstocks)
            # 计算止盈卖出的股票并存入records
            sellstocks = close_all[close_all.ret_rate > stopprofit]
            if len(sellstocks) != 0:
                if log:
                    dk.Logger.info("以下股票由于盈利大于{}被强制卖出: {}".format(stopprofit, sellstocks.index.tolist()))
                sellstocks = sellstocks.rename(columns={'{}_now'.format(price_type): '{}_sell'.format(price_type)})
                sellstocks['date_sell'] = date
                del sellstocks['{}_buy'.format(price_type)]
                records.update(sellstocks)
            bools = (close_all.ret_rate >= stoploss) & (close_all.ret_rate <= stopprofit)
            close_new = close_all[bools]
            if len(close_new) == 0:  # 到期日前股票全部卖完
                break
            del close_new['{}_now'.format(price_type)]
            del close_new['ret_rate']
            cost_info = close_new.copy()
    records = records.dropna()
    records = records.rename(columns={'date': 'date_buy'})
    ret_rate = records['{}_sell'.format(price_type)].sum() / records['{}_buy'.format(price_type)].sum() - 1
    return ret_rate


def back_test_on_given_model(start_date, end_date, cycle, windows, num, model, benchmark="000300.SH"):
    """
    根据给定的mfs模型在指定时间段内按指定换仓周期进行回测
    @start_date <"%Y-%m-%d">: 回测开始日期
    @end_date <"%Y-%m-%d">: 回测结束日期
    @cycle <int>: 换仓周期
    @windows <int>: 计算因子权重的滚动窗口 即根据近多少个交易日进行分组有效性检验
    @num <int>: 持股个数
    @model <function>: 选股模型函数 可选： mfs_by_score
    @benchmark <str>: 基准 hs300
    """

    output = {}
    trading_days = fk.get_trading_days(start_date, end_date)
    start = start_date  # 初始建仓点
    while (trading_days.index(start) + cycle) < len(trading_days):  # 当建仓后cycle个交易日后有值时执行
        end = trading_days[trading_days.index(start) + cycle]
        print('当前建仓日期', start, '当前强制平仓日期', end)
        selected_stocks = model(date=start, windows_step1=windows, num1=num)
        # 获取开始日期和结束日期的收盘价
        model_return = calculate_period_return(start, end, selected_stocks)
        bench_return = calculate_period_return(start, end, [benchmark])
        output[start] = {"model_return": model_return, "hs_300_return": bench_return}
        if trading_days.index(end) + 1 >= len(trading_days):
            break
        start = trading_days[trading_days.index(end) + 1]
    df = pd.DataFrame(output).T
    df1 = df.copy()
    for i in range(df.shape[0]):
        if i == 0:
            df1.iloc[i, :] = 1
        else:
            df1.iloc[i, :] = df1.iloc[i - 1, :] + df.iloc[i, :]
    return output


def back_test_on_given_model_set_stop(start_date, end_date, cycle, windows, num, model, stoploss, stopprofit, benchmark="000300.SH"):
    """
    根据给定的mfs模型在指定时间段内按指定换仓周期进行回测 设置止盈止损点
    @start_date <"%Y-%m-%d">: 回测开始日期
    @end_date <"%Y-%m-%d">: 回测结束日期
    @cycle <int>: 换仓周期
    @windows <int>: 计算因子权重的滚动窗口 即根据近多少个交易日进行分组有效性检验
    @num <int>: 持股个数
    @model <function>: 选股模型函数 可选： mfs_by_score
    @stoploss <float>: 止损率 如=-0.1 即当浮亏率达到10%时卖出
    @stopprofit <float>: 止盈率 如=0.1 即当浮盈率达到10%时卖出
    @benchmark <str>: 基准 hs300
    """

    output = {}
    trading_days = fk.get_trading_days(start_date, end_date)
    start = start_date  # 初始建仓点
    while (trading_days.index(start) + cycle) < len(trading_days):  # 当建仓后cycle个交易日后有值时执行
        end = trading_days[trading_days.index(start) + cycle]
        print('当前建仓日期', start, '当前强制平仓日期', end)
        selected_stocks = model(date=start, windows_step1=windows, num1=num)
        # 获取开始日期和结束日期的收盘价
        model_return = stop_loss_or_profit(sec_ids=selected_stocks, start_date=start, end_date=end,
                                           stoploss=stoploss, stopprofit=stopprofit, price_type='close')
        bench_return = calculate_period_return(start, end, [benchmark])
        output[start] = {"model_return": model_return, "hs_300_return": bench_return}
        if trading_days.index(end) + 1 >= len(trading_days):
            break
        start = trading_days[trading_days.index(end) + 1]
    df = pd.DataFrame(output).T
    df1 = df.copy()
    for i in range(df.shape[0]):
        if i == 0:
            df1.iloc[i, :] = 1
        else:
            df1.iloc[i, :] = df1.iloc[i - 1, :] + df.iloc[i, :]
    return output

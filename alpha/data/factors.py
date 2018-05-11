# -*- coding: utf-8 -*-


#  计算波动率

query = "SELECT date, sec_id, close \
FROM time_series_variables \
WHERE is_st = 0 AND is_trade = 1 \
;"

#  删除所有close为0的records
close1 = close[close.close != 0]


def cal_vol(df, date_num, cycle):
    """
    给定价格和周期计算每只股票滞后周期个交易日的波动率
    @df <dataFrame>: date<datetime.date> sec_id close
    @date <datetime.date, %Y-%m-%d>: 要求波动率的日期
    @cycle <int>: 周期 单位为天
    """
    df1 = df[df.date.le(date_num)]

    def func_vol(x, cycle):
        num = x.count()  # 当前股票在基准日之前的交易日个数
        if num < cycle:  # 如果历史交易天数小于要计算的周期 则返回空值
            return np.nan
        else:
            return x.tail(cycle).std()
    df2 = df1.groupby(['sec_id']).apply(lambda x: func_vol(x.close, cycle))
    df2.name = 'vol_{}days'.format(str(cycle))
    df3 = df2.to_frame()
    df3['date'] = date_num
    df4 = df3.dropna().reset_index()
    return df4


datelist = list(set(close2.date.tolist()))
datelist = sorted(datelist)
output = pd.DataFrame()

for date in datelist:
    df = cal_vol(close2.copy(), date, 5)
    if len(df) != 0:
        output = output.append(df)

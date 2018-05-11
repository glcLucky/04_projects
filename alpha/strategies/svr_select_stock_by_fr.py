# -*- coding: utf-8 -*-

"""
基于SVR模型 以年报中的财务指标为features，股票的年收益率为label 建立SVR模型
target variable: 年收益率
features：
选股范围：
训练期：
测试集：
模型：
参数：


comments
1. 简化起见申万行业分类采取的是最新申万行业，然后匹配到过去，因此并没有考虑某个上市公司的行业变化

"""
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import datetime

from sklearn.decomposition import KernelPCA
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import scale
from sklearn.metrics import r2_score
from sklearn.svm import SVR

import devkit.api as dk

from .. config import(
    USER,
    PASSWORD,
)

conn = dk.MySQLProxy()
conn.connect("root", "123888", "indicator")


#  假设选股时点为2016-05-01 则可获得的最新财报为2015年年报 则建模时间段为 2012——2014三年的年报数据

# 获取2012——2014三年的年报数据 fr_final
query = "SELECT * FROM report_variables1 WHERE (Year(date_report) BETWEEN 2012 AND 2014) AND MONTH(date_report) =12"
fr = conn.query_as_dataframe(query)
fr['date_report'] = fr.date_report.apply(lambda x: str(x))
fr['date_published'] = fr.date_published.apply(lambda x: str(x))
fr_final = fr.copy()

# 获取每只股票年报发布日之后1年的收益率
temp1 = fr_final[['date_published', 'sec_id']].copy()
temp1['year'] = temp1.date_published.apply(lambda x: x[:4])

# 此query可以做初步筛选 剔除st股和次新股以及停牌股份
query = "SELECT date, sec_id, close, traded_days_until_now, is_trade, is_st, stock_float_shares \
FROM time_series_variables \
WHERE is_st=0 AND (date BETWEEN '2013-01-01' AND '2015-4-31') AND traded_days_until_now>400 AND is_trade=1 \
;"
close1 = conn.query_as_dataframe(query)
close1['date'] = close1.date.apply(lambda x: str(x))
close2 = close1[['date', 'sec_id', 'close', 'stock_float_shares']]


# 下面获取每个股票年报发布日当天或之后第一个交易日的股价和一年后最接近的股价
def get_close_price_on_published_day(df_fr, df_close):
    """
    df_fr: <DataFrame>: columns = ['date_published','sec_id']
    df_close: <DataFrame>: columns = [date sec_id  close stock_float_shares]

    """
    df_close['yearmonth'] = df_close.date.apply(lambda x: x[:7])
    df_fr['yearmonth'] = df_fr['date_published'].apply(lambda x: x[:7])
    df1 = df_fr.merge(df_close, how='inner', on=['sec_id', 'yearmonth'])
    df2 = df1.groupby(['sec_id', 'date_published'], as_index=False).apply(lambda x: x[x.date >= x.date_published].head(1))
    df3 = df2.rename(columns={'close': 'close_begin', 'date': 'date_beging'})
    del df3['yearmonth']
    return df3


def get_close_price_after_one_year_on_published_day(df_fr, df_close):
    """
    df_fr: <DataFrame>: columns = ['date_published','sec_id']
    df_close: <DataFrame>: columns = [date sec_id  close stock_float_shares]

    """
    df_close['yearmonth'] = df_close.date.apply(lambda x: x[:7])
    df_fr['date_one_year'] = df_fr.date_published.apply(lambda x: str(int(x[:4]) + 1) + x[4:])  # 1年后的价格
    df_fr['yearmonth'] = df_fr['date_one_year'].apply(lambda x: x[:7])
    df1 = df_fr.merge(df_close, how='inner', on=['sec_id', 'yearmonth'])
    df2 = df1.groupby(['sec_id', 'date_published'], as_index=False).apply(lambda x: x[x.date <= x.date_one_year].tail(1))
    df3 = df2.rename(columns={'close': 'close_ending', 'date': 'date_ending'})
    del df3['yearmonth']
    del df3['date_one_year']
    return df3


flag = fr_final[['date_published', 'sec_id']].copy()

close2 = get_close_price_on_published_day(df_fr=flag.copy(), df_close=close2.copy())  # 加copy是为了防止形参影响实参 并且传递给函数的是可变序列
close3 = get_close_price_after_one_year_on_published_day(df_fr=close2.copy(), df_close=close2.copy())
close_final = close3[['date_published', 'sec_id', 'date_beging', 'close_begin', 'date_ending', 'close_ending', 'stock_float_shares_x', 'stock_float_shares_y']].copy()

close_final['return_rate'] = close_final['close_ending'] / close_final['close_begin'] - 1
close_final["stock_float_shares_mean"] = (close_final["stock_float_shares_x"] + close_final["stock_float_shares_y"]) / 2
df1 = fr_final.merge(close_final, how='inner', on=['date_published', 'sec_id'])

# 剔除银行业和非银金融业
industry = pd.read_csv(r"E:\99_daily\TODAY\industry_sw.csv")
industry['sec_id'] = industry['sec_id'].apply(lambda x: x.split('.')[1] + x.split('.')[0])
industry_map = industry[['sec_id', 'industry_sw']]
df2 = df1.merge(industry_map, how='inner', on=['sec_id'])
df3 = df2[~df2.industry_sw.isin(['银行', '非银金融'])].copy()

# 剔除不必要的变量
train_pre = df3.drop(['sec_id', 'date_report', 'date_published', 'date_beging', 'close_begin', 'date_ending', 'close_ending', 'stock_float_shares_x', 'stock_float_shares_y', 'stock_float_shares_mean', 'industry_sw'], axis=1)

# 剔除有缺失的feature
retained_vars = (train_pre.isnull().sum() == 0)
retained_vars = retained_vars[retained_vars].index.tolist()
train_pre1 = train_pre.loc[:, retained_vars]

y = train_pre2.iloc[:, -1]
X = train_pre2.iloc[:, :-1]#  核主成分降维
kpca = KernelPCA()
kpca.fit(X)

#  通过以下可以判断前15个主成分解释了95%以上的变差

get_we = lambda x: x / x.sum()
get_we(kpca.lambdas_)[:16].sum()

X_transform = kpca.transform(X)[:, :16]  # 降维后的数据 取前15个主成分
#  基于转换后的数据划分数据集
x_train, x_test, y_train, y_test = train_test_split(X_transform, y, test_size=0.33)



# 读取数据集 待整合
features_ts = []  # 时间序列特征
features_fr = []  # 财报特征

# 获取满足条件的股票列表


# 选取每年最后一个交易日的相关信息

query = "SELECT a.sec_id, a.date, a.is_st, a.is_trade, a.traded_days_until_now, a.stock_float_shares a.industry_sw\
FROM stocks_infos as a \
INNER JOIN\
(SELECT sec_id, max(date) as date_max\
    FROM stocks_infos\
    GROUP BY Year(date), sec_id\
) as b\
on a.sec_id=b.sec_id and a.date=b.date_max\
HAVING a.date between '2010-01-01' AND '2015-12-31' \
ORDER BY a.date, a.sec_id\
;\
    "

stocks_info = conn.query_as_dataframe(query)
stocks_info1 = stocks_info[stocks_info.is_trade == 1]  # 剔除停牌股
stocks_info2 = stocks_info1[stocks_info1.is_st == 0]  # 剔除st股
stocks_info3 = stocks_info2[
    ~stocks_info2.industry_sw.isin(["银行", "非银金融"])]  # 剔除金融股
stocks_info4 = stocks_info3[stocks_info3.traded_days_until_now > 400]  # 剔除次新股
stocks_info4 = stocks_info4.sort_values(
    ['date', 'industry_sw', 'stock_float_shares'], ascending=[True, True, False])
stocks_info4['date'] = stocks_info4['date'].apply(lambda x: str(x))
stocks_info5 = stocks_info4.groupby(['date', 'industry_sw'], as_index=False).apply(
    lambda x: x.head(30))  # 按流通市值选取各行业排名前30的企业
stocks_info5['date'] = stocks_info5['date'].apply(
    lambda x: x.split('/')[0] + '-' + x.split('/')[1] + '-' + x.split('/')[2])
stocks_info5['year'] = stocks_info5.date.apply(lambda x: x.split('-')[0])
flag = stocks_info6[['sec_id', 'year']]


# 标的股票列表
sec_ids = get_sec_ids()
df_ts = get_features_ts(sec_id=[], features=features_ts,
                        trading_days=trading_days)
df_fr
df = pd.read_csv(r"E:\99_daily\TODAY\post_process.csv", encoding='gbk')

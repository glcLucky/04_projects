# -*- coding: utf-8 -*-
import pandas as pd
from pandas import DataFrame, Series
import numpy as np
import matplotlib.pyplot as plt

# 建立一个序列
series = pd.Series([1, 3, 5, np.nan, 6, 8])
# 序列的提取
series[1]  # 取series索引为1的值
series.iloc[1]  # 取series第2行的值

# 建立数据框
dates = pd.date_range('20130101', periods=6)
df = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=list("ABCD"))
df
# 建立数据集的另一种方式
df2 = pd.DataFrame({'A': 1.,
                    'B': pd.Timestamp('20130102'),
                    'C': pd.Series(1, index=list(range(4)), dtype='float32'),
                    'D': np.array([3] * 4, dtype='int32'),
                    'E': pd.Categorical(['test', 'train', 'test', 'train']),
                    'F': 'foo'})

df.dtypes  # 显示各个变量的类型

df.index  # 显示数据框的索引
df.columns  # 生成一个变量数组
df.values
df.describe()  # 对于数据的快速统计汇总
df.T  # 对数据的转置

# 排序
df.sort_index(axis=0, ascending=False)
df.sort_index(axis=1, ascending=False)
# 上述排序都是对轴进行排序，axis=0表示对纵轴排序，即索引，axis=1表示对横轴，即变量名
df.sort_values(by=['A', 'B'])
# 上述排序是对值进行排序


# 获取一个单独的列或多个列
df['A']
df[['A', 'B']]
# 利用切片提取行，切片只能对索引用
df[0:2]  # 不包括2，即第3行
df['20130102':'20130104']  # 包括'20130104'
# 即用索引值进行切片时，包括两端值，而用位置切片时，含首不含尾

# 以下通过标签进行选取，逗号之前的是行标签，逗号之后的是列标签
# 用标签定位loc
df.loc[dates[0:2]]  # 如果选取所有的列，可以省去逗号及逗号右边的内容
df.loc[:, ['A', 'B']]
df.loc['20130102':'20130104', ['A', 'B']]

# 用索引定位iloc
df.iloc[3]  # 选择第三行
df.iloc[3:5, 0:2]  # 类似于切片，包括第三行但不包括第5行

# 布尔索引
df[df.A > 0]  # 选取A列大于0的行
df[df > 0]  # 将df中所有小于等于0的值变为NaN

df2 = df.copy()  # 将df copy给df2
df2['E'] = ['one', 'one', 'two', 'twp', 'four', 'therr']  # 在df2中新建一个E列
# df2['E'].astype('str')
df2.dtypes
df2['E'].isin(['two', 'four'])
df2[df2['E'].isin(['two', 'four'])]
df2[df2.E.isin(['two', 'one'])]

# 增加新列
s1 = pd.Series([1, 2, 3, 4, 5, 6], index=pd.date_range('20130102', periods=6))
s1
df['F'] = s1  # 将s1的值添加到数据框df中，命名为F列
df.loc[dates[0], 'A'] = 1
df.iloc[0, 0] = 99
df.loc[:, 'D'] = np.array([5] * len(df))

# reindex: reindex()方法可以对指定轴上的索引进行改变/增加/删除操作，这将返回原始数据的一个拷贝
df
# 利用reindex在df数据集上添加一个空列E
df1 = df.reindex(index=dates[0:4], columns=list(df.columns) + ['E'])
# 利用reindex改变列的位置
df1 = df.reindex(columns=['A', 'C', 'B', 'D'])
# 利用reindex增加一个新行，并采用前向填充法
df4 = df.reindex(index=dates[0:4], columns=['A', 'B'])  # 相当于只取A、B两列

# 删除行（axis=0）或删除列（axis=1）
df_del = df.copy()
df_del.index[2]
df_del.drop(df_del.index[2], axis=0)
df_del.drop(['A', 'D'], axis=1)

# 缺失值处理
# 删除包含缺失的行
df1.dropna(how='any')

# 对缺失值进行填充
df1.fillna(value=5)
# df.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False)
# axis 指 轴，0是行，1是列，
# how 是删除条件：any 任意一个为na则删除整行/列,all 整行/列为na才删除
# inplace 是否在原DataFrame 上进行删除，false为否

# 删除指定列为缺失的所在的行(方法1）
np.isnan(df1['E'])  # 判断F列的是否为缺失值（返回布尔值）
df1[np.isnan(df1['E'])]  # 返回F列为缺失的所在的行
df1[np.isnan(df1['E'])].index  # 返回这些行的索引
df1.drop(df1[np.isnan(df1['E'])].index)  # 在df1删除F列为空的行

# 删除指定列为缺失的所在的行(方法2,简洁）
df1[df1.E.isnull().values == False]

# 观测累加
df.cumsum()
df.apply(np.cumsum)  # 这个累加语句与上面的等价
df.apply(lambda x: x.max() - x.min())  # 求每个维度的极差
df.isnull()

# 频数统计及直方图
# A是分类变量
df['A'].value_counts().plot.bar(color='g', alpha=0.6)
z = pd.Series(np.random.randint(1, 10, 10))
z.value_counts()  # 统计变量z各个取值的频数
z.hist()  # 画出z取值的直方图

# 连接
# np.random.rand（d1,d2,d3...) 返回0-1的均匀分布随机数，括号中的是维度
# np.random.randn（d1,d2,d3...) 返回标准正态分布随机数，括号中的是维度
# np.random.randint（low,high,size) #返回low-high之间的整数均匀分布随机数，size是个数
df5 = pd.DataFrame(np.random.randn(10, 4))
pieces = [df5[:3], df5[3:7], df5[7:]]  # 分割数据集
pd.concat(pieces)  # 合并数据集

score = pd.DataFrame(
    {'name': ['Tom', 'Andy', 'Bob', 'Abby'], 'score': [51, 24, 36, 12]})

id_info = pd.DataFrame(
    {'name1': ['Tom', 'Andy', 'Bob'], 'id': [2734, 2622, 2136]})
id_info.dtypes

pd.merge(score, id_info, left_on='name', right_on='name1', how="outer")
# how的取值有 outer（全连接） inner（内连接） left（左连接） right(右连接）
# left_on right_on  如果两个数据框有相同的键，则可用on

# 纵向连接
test1 = pd.DataFrame(np.random.randn(8, 4), columns=['A', 'B', 'C', 'D'])
test2 = pd.DataFrame(np.random.randn(3, 4) * 3, columns=['A', 'B', 'C', 'D'])
test1.append(test2, ignore_index=True)

# 分组汇总
grade = pd.DataFrame({'sex': ['m', 'f', 'm', 'm', 'f'],
                      'name': ['tom', 'cacy', 'bob', 'jake', 'olivia'],
                      'score1': np.random.randn(5),
                      'score2': np.random.randn(5)})
grade = grade.reindex(columns=['sex', 'name', 'score1', 'score2'])  # 改变列的位置

# 移动平均
pd.rolling_mean(grade['score1'], 2)
ana = grade.groupby(by=['sex', 'name'])
ana.sum()
ana.max()

# pivot table
pivot = pd.DataFrame('A': ['one', 'two', 'three', 'four'] * 3,
                     'B': ['A', 'B', 'C'] * 4
                     'C': ['foo', 'foo', 'foo', 'bar', 'bar', 'bar'] * 2
                     'D': np.random.randn(12)
                     'E': np.random.randn(12))

# index的不可修改性 immutable
index = pd.Index(np.arange(3))
index[2] = 4  # 出错
obj2 = Series([1.5, -2.5, 0], index=index)
obj2.index is index  # 返回True

# 算术运算和数据对齐
s1 = Series([7.3, -2.5, 3.4, 1.5], index=['a', 'c', 'd', 'e'])
s2 = Series([-2.1, 3.6, -1.5, 4, 3.1], index=['a', 'c', 'e', 'f', 'g'])
s1 + s2

df1 = pd.DataFrame(np.arange(9).reshape(3, 3), columns=list(
    'bcd'), index=['Ohio', 'Texas', 'Colorado'])
df2 = pd.DataFrame(np.arange(12).reshape(4, 3), columns=list(
    'bde'), index=['Utah', 'Ohio', 'Texas', 'Oregon'])
df1 + df2  # 根据索引自动匹配相加，匹配不上的变为NaN
# 如果想为不匹配的值填充，可以这样实现
df1.add(df2, fill_value=0)  # Oregon的c值在两个数据框中都没用值，故仍是NaN

# Dataframe和Series之间的运算
arr = np.arange(12.).reshape((3, 4))
# 向下广播，即按列匹配，按行广播
arr[0]
arr - arr[0]

# 实现按行匹配，按列广播的途径
arr[:, 0]
(arr.T - arr[:, 0]).T

frame = pd.DataFrame(np.arange(12).reshape(4, 3), columns=list(
    'bde'), index=['Utah', 'Ohio', 'Texas', 'Oregon'])
series = frame.iloc[0]

# 将series的索引匹配dataframe的列，然后沿着行向下广播
frame - series
frame.sub(series, axis=1)  # 与上述等价
# 如果你想匹配行并且在列上广播，可通过这样实现
series3 = frame['d']
frame.sub(series3, axis=0)
# 常见的运算符号：add，sub，div，mul（乘）

# 以列联表的形式显示数据 margin表示是否求和
aa = pd.crosstab(df['rs2273298'], df["y"], margins=True)

# copy
b = a["A"]
c = a["B"]
如果不加copy，b和c仅仅是对象a不同部分的索引，本质上仍是a, 改变a、b会影响到a
b = a["A"].copy()
c = a["B"].copy()
加了copy之后，则b、c净与a没有关系

# 例子
x = pd.DataFrame({"A": [1., 2., 3.], "B": [2, 1, 2]})
y1 = x['A']
y2 = x['A'].copy()
x.loc[x['A'] > 1, "A"] = 99  # 在原数据集中将变量A大于1的值设为99 必须使用loc不能直接引用 会影响到y1 但不影响y2


# 读取excle文件
def load_excel_data(filename):
    """
    从excel文件中读取各个sheet 存储在字典df_all当中
    """
    data = pd.ExcelFile(filename)
    print(data.sheet_names)
    df_all = {}
    for sheet in data.sheet_names:
        df_all[sheet] = data.parse(sheet)
    return df_all


#  基于pandas中的列中的值从DataFrame中选择行

# 要选择列值等于标量some​​_value的行，请使用==：
df.loc[df['column_name'] == some_value]

# 要选择其列值在可迭代值some_values中的行，请使用isin：
df.loc[df['column_name'].isin(some_values)]

# 要选择列值不等于some_value的行，请使用！=：
df.loc[df['column_name'] != some_value]

# isin返回一个布尔系列，所以要选择值不在some_values的行，使用〜来否定布尔系列：
df[~df['column_name'].isin(some_values)]  # 注意否定布尔序列是~ 而不是！


output = t_sf_a[t_sf_a.date.between(left=start_date, right=end_date, inclusive=True)]

# 缺失值填补


def handle_outlier(x):
    x[np.abs(x) > 3] = 3
    return x
# lambda运行原理是每次读取一列
df3 = df2.apply(lambda x: handle_outlier(x))

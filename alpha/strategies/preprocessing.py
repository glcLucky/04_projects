# -*- coding: utf-8 -*-

"""
preprocessing.py
对数据集进行预处理

思路:
1. 对训练集进行预处理
2. 对测试集进行与训练集同样的预处理
"""
import pickle
import os
import pandas as pd


def wash_train_data(df_train, DATAID, recalculate=False):
    """
    对训练集进行数据清洗
    @df_train <DataFrame>:待处理特征向量
    @DATAID <INT>： 数据集编号
    @recalculate <bool>: 如果已经存在 是否重新计算均值和标准差
    """
    # 统计标准化
    if os.path.exists(r"E:\07_data\02_factor\preprocessing\std_info_{}.txt".format(DATAID)) and not recalculate:
        print("STD_INFO has already existed")
        f = open(r"E:\07_data\02_factor\preprocessing\std_info_{}.txt".format(DATAID), 'rb')  
        std_info=pickle.load(f)
        train_mean = std_info['mean']
        train_std = std_info['std']
    else:
        train_mean = df_train.mean()
        train_std = df_train.std()
        f = open(r"E:\07_data\02_factor\preprocessing\std_info_{}.txt".format(DATAID), 'wb')
        std_info = {"mean": train_mean, "std": train_std}
        pickle.dump(std_info, f, 0)
        f.close()
    df_train = (df_train - train_mean) / train_std
    return df_train
    return df_train


def wash_test_data(df_test, DATAID):
    """
    对测试集进行数据清洗
    @df_test <DataFrame>:待处理特征向量
    @DATAID <INT>： 数据集编号
    """
    # 统计标准化
    train_mean = df_test.mean()
    train_std = df_test.std()
    f = open(r"E:\07_data\02_factor\preprocessing\std_info_{}.txt".format(DATAID), 'rb')
    std_info = pickle.load(f)
    f.close()
    df_test = (df_test - std_info['mean']) / std_info['std']
    return df_test

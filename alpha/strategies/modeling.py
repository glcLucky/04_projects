# -*- coding: utf-8 -*-

"""
select_stocls_by_ML.py
基于机器学习方法的多因子选股模型

思路:
1. 基于财务指标选出具有长期收益的股票作为备选股票池
2. 利用机器学习方法，使用量价指标从股票池中挖掘短期强势的股票作为持仓股票
"""

import os
import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn import metrics
import matplotlib.pyplot as plt
from .. config import DB_PATH


def XGB_classfier_fit(df_features, df_label, params, dataID, num_boost_round=200, refit=False, name="XGB"):
    """
    训练XGB分类模型
    @df_features <DataFrame>: 清洗后的特征向量
    @df_label <DataFrame>: 目标变量
    @param <dict>: XGB模型参数
    @dataID <int>: 数据集编号
    @num_boost_round <int>: 迭代次数 重要参数
    @refit <bool>: 如果已经存在 是否重新训练模型
    @return 训练好后的xgb模型
    """
    model_root_path = os.path.join(DB_PATH, r"model\{}".format(name))
    if not os.path.exists(model_root_path):
        os.makedirs(model_root_path)
    model_path = os.path.join(model_root_path, "{}_{}.model".format(name, dataID))
    if os.path.exists(model_path) and not refit:
        print("MODEL has already been fitted")
        bst = xgb.Booster()
        bst.load_model(model_path)
        return bst
    else:
        dtrain = xgb.DMatrix(df_features.values, label=df_label.values)
        bst = xgb.train(params=params, dtrain=dtrain, num_boost_round=num_boost_round, verbose_eval=False)
        bst.save_model(model_path)
        return bst


def XGB_classfier_predict_prob(XGB_model, df_features):
    """
    利用训练好的XGB模型预测概率
    @XGB_model <model func>: 训练好的XGB模型
    @df_features <DataFrame>: 特征向量
    @return 样本为正例的概率向量
    """
    df_features = xgb.DMatrix(df_features.values)
    y_scores = XGB_model.predict(df_features)
    return y_scores





def plot_roc_curve(y, y_scores, ds_type, dataID, label=None, override=False):
    """
    绘制roc曲线
    @y <np.array>: 目标变量向量
    @y_scores <np.array>: 标签为正例的概率向量
    @ds_type <str>: 数据集类型 测试集 or 训练集
    """
    root_path = os.path.join(DB_PATH, r"evaluation\roc_curve\{}".format(dataID))
    if not os.path.exists(root_path):
        os.makedirs(root_path)
    roc_path = os.path.join(root_path, "{}.png".format(ds_type))
    if os.path.exists(roc_path) and not override:
        print("该roc曲线已经存在")
        return
    fpr, tpr, thresholds = metrics.roc_curve(y, y_scores)
    auc = metrics.roc_auc_score(y, y_scores)
    fig, ax = plt.subplots()
    fig.set_size_inches(20, 10)
    ax.plot([0, 1], [0, 1], 'k--')
    plt.axis([0, 1, 0, 1])
    ax.plot(fpr, tpr, linewidth=2, label=label)
    plt.xlabel('False Positive Rate', fontsize=22)
    plt.ylabel('True Positive Rate', fontsize=22)
    plt.title("基于{}的ROC曲线 AUC={}".format(ds_type, auc), fontsize=22)
    plt.savefig(roc_path)

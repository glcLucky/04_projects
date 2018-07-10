# -*- coding: utf-8 -*-

"""
classification.py
"""

from sklearn import linear_model  # 线性模型
from sklearn.svm import SVC


def fit_LR(features, target):
    """
    训练LR模型
    """
    Logreg = linear_model.LogisticRegression()
    return Logreg.fit(features, target)


def fit_SVC(features, target, params):
    """
    训练SVM模型
    可选参数：
    @C <float>: 经验风险惩罚因子 越大对当前样本误分类的惩罚越大
    @kernel <str>: 核函数 默认为rbf  'linear', 'poly', 'rbf', 'sigmoid', 'precomputed'
    @gamma <float>: 默认为'auto' 等于特征数的倒数 Kernel coefficient for ‘rbf’, ‘poly’ and ‘sigmoid’
    @coef0 <float>: 默认为0 Independent term in kernel function. It is only significant in ‘poly’ and ‘sigmoid’
    @probability <bool>: 是否输出概率 默认为False
    @tol <float>: Tolerance for stopping criterion. 默认为1e-3
    """
    svc = SVC(**params)
    return svc.fit(features, target)

# -*- coding: utf-8 -*-

"""
classification.py
"""

from sklearn import linear_model  # 线性模型


def fit_LR(features, target):
    """
    训练LR模型
    """
    Logreg = linear_model.LogisticRegression()
    return Logreg.fit(features, target)

# -*- coding: utf-8 -*-

"""
formula.py

因子的计算公式，输出未经统计处理的因子值，形如 calculate_raw_<factor_name>

@author: Jasper Gui
@email: jasper.gui@outlook.com
@date: 2018.03.08
"""

import numpy as np


def calculate_raw_BETA(context):
    return context.rename(columns={"BETA_100W": "BETA"})

def calculate_raw_DIVIDENDYIELD2(context):
    return context

def calculate_raw_EV2_TO_EBITDA(context):
    return context

def calculate_raw_PB_LF(context):
    return context

def calculate_raw_PCF_OCF_TTM(context):
    return context

def calculate_raw_PS_TTM(context):
    return context

def calculate_raw_VAL_PE_DEDUCTED_TTM(context):
    return context

def calculate_raw_CURRENT(context):
    return context

def calculate_raw_DEBTTOASSETS(context):
    context["DEBTTOASSETS"] = context["DEBTTOASSETS"].apply(lambda x: np.log(x) if x > 0. else x)
    return context


def calculate_raw_EBITOFREVENUE(context):
    context['EBITOFREVENUE'] = context["EBIT2_TTM"] / context["OR_TTM2"]
    data_raw = context.loc[:, ["sec_id", "EBITOFREVENUE"]].copy()
    return data_raw


def calculate_raw_GROWTH(context):
    # TODO: 应当是环比增长率，架构复杂
    context['GROWTH'] = context['OR_TTM2'] / context['OR_TTM2_1'] - 1
    data_raw = context.loc[:, ['sec_id', 'GROWTH']].copy()
    return data_raw


def calculate_raw_LEVERAGE(context):
    context["LEVERAGE"] = context['DEBTTOASSETS'] * 0.7 + context['CURRENT'] * 0.3
    data_raw = context.loc[:, ["sec_id", "LEVERAGE"]].copy()
    return data_raw


def calculate_raw_LIQ(context):
    context["LIQ"] = np.log(context["AVG_TURN_ND"])
    data_raw = context.loc[:, ["sec_id", "LIQ"]].copy()
    return data_raw


def calculate_raw_MOM(context):
    return context.rename(columns={"ANNUALYEILD_100W": "MOM"})


def calculate_raw_PROFIT(context):
    context["PROFIT"] = context['ROE'] * 0.7 + context['EBITOFREVENUE'] * 0.3
    data_raw = context.loc[:, ["sec_id", "PROFIT"]].copy()
    return data_raw


def calculate_raw_ROE(context):
    return context.rename(columns={"ROE_TTM3": "ROE"})


def calculate_raw_SIZE(context):
    context["SIZE"] = np.log(context["MKT_CAP_FLOAT"])
    data_raw = context.loc[:, ["sec_id", "SIZE"]].copy()
    return data_raw


def calculate_raw_VALUE(context):
    context["VALUE"] = context["PB_LF"]**(-1)
    data_raw = context.loc[:, ["sec_id", "VALUE"]].copy()
    return data_raw


def calculate_raw_VOL(context):
    return context.rename(columns={"ANNUALSTDEVR_100W": "VOL"})

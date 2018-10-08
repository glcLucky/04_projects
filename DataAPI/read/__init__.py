# -*- coding: utf-8 -*-

"""
read

读数据库相关函数

@author: Jasper Gui
@email: wuyd@swsresearch.com
@date: 2017.12.11
"""

from . import (
    index_contents,
    industry,
    indicator,
    factor,
    factor_return,
    calendar,
)

from . calendar import (
    get_report_days,
    get_trading_days,
    get_monthly_last_trading_days,
    get_weekly_last_trading_days,
    get_weekly_and_monthly_last_trading_days,
)

from . index_contents import (
    get_index_contents,
    get_index_contents_on_multidays,
    get_index_weights,
    get_secs_name,
)

from . industry import (
    get_secs_industry,
    get_secs_industry_SWL1,
)

from . indicator import (
    get_secs_indicator,
    get_secs_indicator_on_multidays,
    get_adjusted_close_price,
)

from . factor import (
    get_secs_factor,
    get_secs_factor_on_multidays,
)

from . factor_return import (
    get_factor_return_daily,
    get_factor_return_cum,
    plot_single_factor_return_cum,
)


__all__ = [
    "get_report_days",
    "get_trading_days",
    "get_monthly_last_trading_days",
    "get_weekly_last_trading_days",
    "get_weekly_and_monthly_last_trading_days",

    "get_index_contents",
    "get_index_contents_on_multidays",
    "get_index_weights",
    "get_secs_name",

    "get_secs_industry",
    "get_secs_industry_SWL1",

    "get_secs_indicator",
    "get_secs_indicator_on_multidays",
    "get_adjusted_close_price",

    "get_secs_factor",
    "get_secs_factor_on_multidays",

    "get_factor_return_daily",
    "get_factor_return_cum",
    "plot_single_factor_return_cum",
]

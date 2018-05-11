# -*- coding: utf-8 -*-

"""
api.py

接口

@author: Wu Yudi
@email: wuyd@swsresearch.com
@date: 2017.01.10
"""

from . wind_api import (
    get_trading_days,
    get_index_contents,
    get_secs_name,
    get_sector_contents,
    get_secs_liqshare,
    get_secs_market_cap,
)

from . wind_price_apis import (
    get_single_attribute,
    get_daily_single_attribute,
    get_single_day_attributes,
    get_daily_prices,
    get_single_day_prices,
)

from . wind_industry_apis import (
    get_secs_industry,
    get_secs_industry_gics,
    get_secs_industry_sw,

)

__all__ = [
    "get_trading_days",
    "get_index_contents",
    "get_secs_name",
    "get_sector_contents",
    "get_secs_liqshare",
    "get_secs_market_cap",

    "get_single_attribute",
    "get_daily_single_attribute",
    "get_single_day_attributes",
    "get_daily_prices",
    "get_single_day_prices",

    "get_secs_industry",
    "get_secs_industry_gics",
    "get_secs_industry_sw",
]

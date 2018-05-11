# -*- coding: utf-8 -*-

"""
load

从数据源载入数据

@author: Wu Yudi
@email: wuyd@swsresearch.com
@date: 2017.12.11
"""

from . import (
    index_contents,
    indicator,
    industry,
    factor,
    factor_return,
)

from . index_contents import (
    load_index_contents_from_wind,
    load_index_contents_and_weights_from_wind,
)

from . indicator import (
    load_single_indicator_on_single_day_from_wind,
)

from . industry import (
    load_secs_industry_sw_from_wind,
    load_secs_industry_gics_from_wind,
)

from . factor import (
    load_single_factor_on_single_day,
)

from . factor_return import (
    load_single_factor_return_on_multidays,
)


__all__ = [
    "load_index_contents_from_wind",
    "load_index_contents_and_weights_from_wind",
    "load_single_indicator_on_single_day_from_wind",
    "load_secs_industry_sw_from_wind",
    "load_secs_industry_gics_from_wind",
    "load_single_factor_on_single_day",
    "load_single_factor_return_on_multidays",
]

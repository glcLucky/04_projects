WRITE
======

**index_contents.py**

- update_index_contents(index_code, trading_days=[], override=False, log=True):

    从Wind更新index_contents相关数据

    @index_code (<str>): 要更新的指标
    @trading_days (['%Y-%m-%d']): 传入的日期列表
    @override （<Bool>): 是否覆盖旧数据 默认为False 表示不覆盖
    @log (<Bool>): 是否打印log

**industry.py**

- update_secs_industry_sw(industry, trading_days=[], override=False):
    
    从Wind更新某指数成分股申万一级行业数据

    @industry (<str>): 指数名称
    @trading_days (<['%Y-%m-%d']): 日期列表
    @override (<Bool>): 是否覆盖原记录 默认为False 表示不覆盖
    
- update_secs_industry_gics(industry, trading_days=[], override=False):
    
    从Wind更新某指数成分股GICS一级行业数据

    @industry (<str>): 指数名称
    @trading_days (<['%Y-%m-%d']): 日期列表
    @override (<Bool>): 是否覆盖原记录 默认为False 表示不覆盖

**indicator.py** 

- update_single_indicator(indicator, trading_days=[], override=False, log=True):

    更新单个indicator的指定日期列表的数据

    @indicator (<str>): 单个indicator的名称
    @trading_days ([%Y-%m-%d]): 日期列表
    @override (<Bool>): 是否覆盖原记录 默认为False 表示不覆盖

- update_indicators(indicators=[], trading_days=[], override=False, log=True):

    更新多个indicator的指定日期列表的数据

    @indicators (<list>): indicator的名称构成的列表
    @trading_days ([%Y-%m-%d]): 日期列表
    @override (<Bool>): 是否覆盖原记录 默认为False 表示不覆盖
    @log (<Bool>): 是否打印log

**factor.py**

- update_single_factor(factor, trading_days=[], override=False, log=True):
    
    更新单个factor的指定日期列表的数据

    @factor (<str>):factor名称
    @trading_days ([%Y-%m-%d]): 日期列表
    @override (<Bool>): 是否覆盖原记录 默认为False 表示不覆盖
    @log (<Bool>): 是否打印log

- update_factors(factors=[], trading_days=[], override=False, log=True):

    更新多个factor的指定日期列表的数据

    @factors (<list>):factor名称构成的列表
    @trading_days ([%Y-%m-%d]): 日期列表
    @override (<Bool>): 是否覆盖原记录 默认为False 表示不覆盖
    @log (<Bool>): 是否打印log

**factor_return.py**

- update_single_factor_return(factor_return, trading_days=[], group_num=10, log=True):

    根据trading_days更新factor_return数据

    @factor_return (<str>): factor的名称
    @trading_days (<[%Y-%m-%d]>) : 日期列表
    @group_num (<int>): 分组个数

- update_factors_return(factors_ret_to_update=[], trading_days=[], group_num=10, log=True):

    根据trading_days更新factor_return数据

    @factors_ret_to_update (<list>):  factor列表
    @trading_days (<[%Y-%m-%d]>) : 日期列表
    @group_num (<int>): 分组个数
    @log (<Bool>): 是否打印log


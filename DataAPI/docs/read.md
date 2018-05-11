READ
====

**index_contents.py**

- get_index_contents(index_code, date, log=True):
    
    读取某日期某指数全部股票列表

    @index_code (str): 要读取的指标编码 可选代码: ['A','H','000905.SH','000300.SH','000016.SH','HSI.HI']
    @date ('%Y-%m-%d'): 单个日期
    @log (Bool): 是否打印log
    :return (list): 股票代码列表
    

- get_index_contents_on_multidays(index_code, trading_days, log=True):
    
    读取多个日期某指数全部股票列表

    @index_code (str): 要读取的指标编码 可选代码: ['A','H','000905.SH','000300.SH','000016.SH','HSI.HI']
    @trading_days (['%Y-%m-%d']): 日期列表
    @log (Bool): 是否打印log
    :return: ({date: list}), key为date value为 股票代码列表
    

- get_index_weights(index_code, date):
    
    读取某日期某指数成分股的权重列表

    @index_code (str): 要读取的指标编码 可选代码: ['A','H','000905.SH','000300.SH','000016.SH','HSI.HI']
    @date (%Y-%m-%d): 单个日期
    :return: {sec_id: weight}


- get_A_secs_name(sec_ids=[]):

    获取最新日期A股股票名称，数据格式为 {股票代码：股票名称}

    @sec_id (list): 股票列表 默认为空 表示最新日期的所有A股
    :return: {sec_id: sec_name}


- get_H_secs_name(sec_ids=[]):

    获取最新日期全H股股票名称，数据格式为 {股票代码：股票名称}

    @sec_id (list): 股票列表 默认为空 表示最新日期的所有h股
    :return: {sec_id: sec_name}

- get_secs_name(sec_ids=[]):

    获取最新日期股票名称，自动处理A股和H股，数据格式为 {股票代码：股票名称}

    @sec_id (list): 股票列表 默认为空 表示最新日期的所有A股和H股
    :return: {sec_id: sec_name}


---

**industry.py**

- get_secs_industry(date="", sec_ids=[], industry_code="A_SWL1"):

    获取某日期某些股票的的行业分类信息，数据格式 {股票代码：行业分类}

    @date: (<%Y-%m-%d>) 单个日期
    @sec_id: (<list>) 股票列表
    @industry_code (<str>): 子数据库名称 默认为A_SWL1 可选名称:["A_SWL1","H_SWL1",]



- get_secs_industry_SWL1(sec_ids=[], date=""):
    
    获取某日期某些股票的的申万一级行业分类信息，自动处理A股和H股，数据格式 {股票代码：行业分类}

    @sec_id: (list) 股票列表
    @date: (%Y-%m-%d) 单个日期
    

---
    
**indicator.py** 

- get_secs_indicator(indicator, sec_ids=[], date='', log=True):

    从本地数据库中获取单个日期的单个indicator的值，并返回 DataFrame

    @indicator (str): 单个indicator
    @date ('%Y-%m-%d'): 单个日期
    @sec_ids (list): 支持多个股票查询，默认为[]，表示查询范围是全A股
    @log (Bool): 是否打印log
    :return: Dataframe 列为indicator名，index为sec_id


- get_secs_indicator_on_multidays(indicator, sec_ids=[], trading_days=[], log=True):

    从本地数据库中获取一段日期的单个indicator的值，并返回 dict of DataFrame

    @indicator (str): 单个indicator
    @sec_ids (list): 支持多个股票查询，默认为[]，表示查询范围是全A股
    @trading_days (["%Y-%m-%d"]): 日期列表
    @log (Bool): 是否打印log
    :return: {date: Dataframe}，其中 DataFrame 列为indicator名，index为sec_id


- get_adjusted_close_price(sec_ids=[], date=""):
    
    从本地数据库中获取某个日期复权后的收盘价，并返回dataframe

    @sec_ids (list): 支持多个股票查询，默认为[],表示查询范围是全A股
    @date ("%Y-%m-%d"): 单个日期 默认为''
    :return: DataFrame，index为sec_id columns为CLOSE (复权后)

---

**factor.py**

- get_secs_factor(factor, date='', sec_ids=[], log=True):
    
    从本地数据库中获取单个日期的单个factor的值，并返回 DataFrame

    @factor (str): 单个factor
    @date ('%Y-%m-%d'): 单个日期
    @sec_ids (list): 支持多个股票查询，默认为[]，表示查询范围是全A股
    @log (Bool): 是否打印log
    :return: Dataframe 列为factor名，index为sec_id
    

- get_secs_factor_on_multidays(factor, trading_days=[], sec_ids=[], log=True):
    
    从本地数据库中获取一段日期的单个factor的值，并返回 dict of DataFrame

    @factor (str): 单个factor
    @sec_ids (list): 支持多个股票查询，默认为[]，表示查询范围是全A股
    @trading_days (["%Y-%m-%d"]): 日期列表
    @log (Bool): 是否打印log
    :return: {date: Dataframe}，其中 DataFrame 列为factor名，index为sec_id

---

**factor_return.py**

- get_factor_return_daily(factor_return_name, trading_days=[]):

    从本地数据库中获取某段日期某个factor_return的日收益率

    @factor_return_name (str): factor名称
    @trading_days (['%Y-%m-%d']): 日期列表
    :return: DataFrame  index:date columns:sec_id group01-group10 factor


- get_factor_return_cum(factor_return_name, trading_days=[]):

    从本地数据库中获取某段日期某个factor_return的累计收益率
    
    @factor_return_name (str): factor名称
    @trading_days (['%Y-%m-%d']) : 日期列表
    :return: DataFrame, index: date, columns: [sec_id group01-group10 factor]


- plot_single_factor_return_cum(factor_return_name_list, trading_days=[], save_plot_path=""):

    绘制多个factor_return的累计收益率图并存放于指定位置

    @factor_return_name_list (list): factor列表
    @trading_days (['%Y-%m-%d']) : 日期列表
    @save_plot_path (str): 存放路径

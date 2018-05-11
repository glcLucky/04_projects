LOAD
====

**index_contents.py**

- load_index_contents_from_wind(index_code, date):

    从wind下载某天某市场的全部股票数据

    @index_code (str): 指数代码 可选列表 A:全A股 H:全H股 HSI.HI:恒生指数
    @date ("%Y-%m-%d"): 单个日期
    :return: DataFrame, columns=['sec_id', 'sec_name']


- load_index_contents_and_weights_from_wind(index_code, date):

    从wind下载某天某指数成分股数据及权重
    
    @index_code (str): 指数编码 可选：000300.SH
    @date (%Y-%m-%d): 单个日期
    :return: DataFrame, columns=['sec_id', 'sec_name', 'weight']

---

**industry.py**

- load_secs_industry_sw_from_wind(index_code, date, level=1):

    从Wind更新指定index成分股的申万行业数据

    @index_code (str): 指数代码 可选代码: "A_SWL1" "H_SWL1"
    @date (%Y-%m-%d): 单个日期
    @level (int): 行业级数 默认为1 表示为申万1级行业分类
    :return: (dict of str): 键是证券代码，值是行业名称


- load_secs_industry_gics_from_wind(index_code, date, level=1):

    从Wind更新指定index成分股的gics行业数据

    @index_code (str):  "H_GICSL1"
    @date (%Y-%m-%d):  单个日期
    @level (int): 行业级数 默认为1 表示为申万1级行业分类
    :return: (dict of str): 键是证券代码，值是行业名称

---
    
**indicator.py** 

- load_single_indicator_on_single_day_from_wind(indicator, date):

    从wind上下载某个指定日期的指标

    @indicator (str): 指标名称,仅支持单个indicator传递
    @date ("%Y-%m-%d): 单个日期
    return: DataFrame，columns=['sec_id','indicator_name']

---

**factor.py**

- load_single_factor_on_single_day(factor, date):

    加载单个日期单个factor的信息

    @factor (str): 指标名称,仅支持单个indicator传递
    @date ("%Y-%m-%d"): 单个日期
    :return: DataFrame，columns=['sec_id','factor_name']

---

**factor_return.py**

- load_single_factor_return_on_multidays(factor, trading_days, group_num=10):

    加载单个日期单个factor的return信息

    @factor (str):  指标名称
    @trading_days (['%Y-%m-%d']): 日期列表
    @group_num (int): 分组个数 默认为10
    return: DataFrame，列名:date group01-group-10 factor_return



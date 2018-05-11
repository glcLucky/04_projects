SYNTAX STANDARD
=================

- 空格和空行的用法：PEP-8

- 文件头上的 docstring 里的 FUNCTION LIST 要带参数

- import 顺序：内置库 - 第三方库 - 自有第三方库 - 本库，每个块间空行

- 全局变量于 import 代码块后定义，全大写字母

- CHANGELOG.md, README.md 放在包的根目录下

- docstring 格式：

    def function(a, b, c=x):
        """
        函数用途

        @a (<a的类型>): <a的含义>
        @b ...
        return (<return的类型>): <return的含义>
        """

        <codes>

- 变更已有函数的参数顺序及名字需要向上级汇报；可以任意新增函数，必须在docstring中新增及在CHANGELOG中注明；定期确定命名规范，确定之后视为已有函数

-----

TIPS
====

TODO
====

- DataAPI封装,去依赖

--------

CHANGE LOG
==========

## 2018-03-13

- 重构 index_contents 相关部分，解决A股与港股的数据存储类型不同导致的架构不同

- 重构 industry 相关部分，解决A股与港股的数据存储类型不同导致的架构不同

- 更改原 db_utils.py 为 sql_utils.py，重构 create_db 系列函数为 create_table，在涉及 sql 的 write 系列函数里都增加自动建表逻辑

- 更改新 db_utils.py，主要为打开文件夹相关操作

- 更改 read_schema.py 为 io.py，新增 save_schema()

- 更改各种 notation 和变量命名，尽量统一

## 2018-03-12

- 数据统一更新到 2018-03-01，重刷 factor 和 factor_return

## 2018-03-05 ~ 2018-03-09

- 部分重构：
    
    - 更改 db/factor/schema 中 context 的数据类型

    - 更改 factor 下文件架构为 calculate.py, const.py, formula.py 和 mapping.py，

    - 新增 miscallaneous 模块，主要为了防止放入 utils 时会导致循环引用

    - 更改 utils 下文件架构为 data_utils.py, datetime_utils.py, db_utils.py, file_utils.py, misc_utils.py

    - 所有 sql 架构采用 with 上下文写法

    - 异常抛出机制略有改动

## 2018-02-26 ~ 2018-03-04

- 在factor_return的write函数中增加了对更新日期的判断 如果更新日期有超过已经存在factor记录的日期，会报出

- 写完并调试通过了factor相关的三个函数

- 写完并调试通过了indicator相关的三个函数：
    - 可以读多支股票多个date
    - sec_ids为空时从index_ contents中读取当日全A股列表
    - 按年整批读取，而不是按日读取

- 增强了write函数
    - 判断是否已经存在时按年判断 而不是之前的按日判断
    - sec_ids为空时从index_contents中读取当日全A股列表
    - 按年整批读取，而不是按日读取

- 完善了schema的更新程序 测试通过

- 写完并调试通过了index_contents相关函数


## 2018-02-26

- [MODIFY] 修复了read/index_contents中的get_A_secs_name函数

- [MODIFY] 修复了index_contents csv转db weight缺失问题 改用pd.read_csv读

- [MODIFY] 修改了load industry的参数 index_code->market 

- [MODIFY] 修改了indicator factor的write函数 增加了sql下override的功能 修改了程序确保及时关掉数据库

- [MODIFY] 修改了所有数据库的read函数 确保能从sql化后的数据中读出数据


## 2018-01-30

-[DEV] 新增indicator 加上成交额  也加上了交易量 done

-[DEV] 新增index_contents: sz50 zz500  done

-[DEBUG] 注意在每段程序中验证合法性 done

-[DEBUG] 从schema中验证数据库是否存在 done

-[DEV] 添加新增数据的shcema及更新程序 done

-[DEV] index_contents 模仿 indicator 和 factor 的做法 done


## 2018-01-26

- [DEV] 完善了index_contents相关的API 将index扩充为 A H 000300.SH HSI.HI四种，其中HSI.HI无法取得权重


## 2018-01-25

- [MODIFY] 将load_A_contents和load_hs300_contents统一到load_index_contents函数 不过办法有点蠢，待改进

- [MODIFY] 修改了原有 industry的write函数  去除了在write中直接调用Windapi 
        增加了load_secs_industry_sw_from_wind函数  负责从wind上下载相应数据
        问题:使所有的下载数据不依赖于WindAPI?
        
- [DEV] 将周期改为天，增加了所有相应的数据，由于额度限制 indicator中的PSttm VAL_PE_DEDUCTED_TTM PB_LF
        但只影响factor中的value
        
- [MODIFY] 将update_schema函数中的indicator和factor合并成一个

- [MODIFY] config.path 解耦

- [MODIFY] 完善了write_indicator中trading_days的处理:区分财报数据和时间序列数据，对财报数据取报告日 
    对时间序列数据取交易日，然后与trading_days取交集。


## 2018-01-24

- [DEV] 新建schema模块 负责schema相关的读写任务

- [MODIFY] calculate_factors 的进一步抽象 增加proprocess_data函数

- [MODIFY] factor_return 命名问题 schema 和 列名 都直接命名成 factor本身


## 2018-01-18

- 修改 get_close_price_adjusted() 为 get_adjusted_close_price()，且输出列名改为 CLOSE

- 更新 maintain.ipynb，拆分为 DB - Update Basic 和 DB - Update Factor

- factor 和 factor_return 的修改类似 indicator

- 修改 write/indicator.py 中 update_indicator_data() 为 update_single_indicator()

- 修改 update_single_indicator() 中调用 update_indicator_schema 的位置，修改打印信息

- 新增 update_indicators()

- [TODO] 完善maintain函数 总结write_factor_return所用到的思想

- [MODIFY] 纠正了在计算factor_return时的重大错误 在load_factor_return函数中 计算date_pre时误用trading_days[i-1] 实际上应当是i 因为enumerate返回的是0,1,2，...,而不是对应日期在trading_days中的索引。纠正错误后，size_return图发生较大变化，在2017年4月-9月中旬，大盘股表现的确优于小盘股，这符合预期，但10月份之后小盘股反弹较大 甚至超过大盘股的收益

- [MODIFY] 修正了get_factor_return_cum函数 将传入trading_days的起始值累计收益赋为1  从第二天开始计算收益

- [DEV] 完善了factor_return的write函数 包含了多种可能  测试通过


## 2018-01-17

- [TODO] update_factor_return时，传入的trading_days的各种情况尚未处理好 这里假设全部override 且trading_days是连续同周期的 为了方便编程，可以只规定几种常用的更新形式 对于不满足条件的更新print出信息。

- [MODIFY] 发现SIZE等一些factor严重不服从正态分布，通过对一些factor取对数很大程度上改变数据的偏斜程度

- [MODIFY] 发现计算factor_return时受极端值影响较大，且取对数或者小幅度调整winsorize的阈值并不改变factor

return的值，因为这两者仅仅改变了数据绝对数值的大小，并不影响相对排名，所以并不影响分组，所以计算出来的return是一样的。 但是通过在计算return时剔除极端值，会大大提高因子的分层有效性。


## 2018-01-16

- [MODIFY] 修改DataAPI\utils\update_schema.py 误写了两个update date 将第一个update_date改成end date


## 2018-01-15

- [DEV] 确定了factor_return的wirite、load、和read编写框架。

- [DEV] 完成了factor_return的schema的设计

- [DEV] 完成了factor_return的write和load函数，计算出了所有factor的return信息。


## 2018-01-12

- [DEV] 完成了所有factor的计算工作

- [DEV] 开始开发factor_return


## 2018-01-11

-[DEV] 在indicator和factor的read函数中增加了一些print信息：传入多少个date，有多少文件已经存在，实际更新了多少个文件

-[MODIFY] 在那些用到财务报表数据的factor计算中，在非报告日，引用上一个报告日的数据，并且加入了考虑新股的情况 将新股赋为空值

-[MODIFY] 在缺失过多需要copy上一个文件时加入了考虑新股的情况 将新股赋为空值


## 2018-01-10

-[DEV] 开发了DataAPI\factor\calculate_factors.py中的所有factor函数，测试通过，并生成了相关数据集

-[DEV] 重新设计了load 使load仅仅负责传输factor名字到calculate函数里。将类型判断、factor构成及运算都植入calculate_XX相关函数里。


## 2018-01-09

-[DEV] 优化了DataAPI\load\factor.py中的load_single_factor_on_single_day函数 加上了对严重缺失情况的考虑，当数据缺失率超过30%时 直接copy取最近一次记录。

-[DEV] 开发了DataAPI\write\factor.py中的update_factor_data函数，测试通过。

-[DEV] 开发了DataAPI\read\factor.py中的get_secs_factor函数，测试通过。

-[DEV] 开发了DataAPI\factor\calculate_factors.py中的calculate_EBITOFREVENUEE函数，测试通过。

-[DEV] 开发了DataAPI\factor\calculate_factors.py中的calculate_EBITOFREVENUEE函数，测试通过。


## 2017-12-29

- [DEBUG] finkit/datetime_utils/fetch中的get_weekly_and_monthly_last_trading_days有问题？？？fetch出的结果不对 已修正：and -> or
- [DEV] 在DataAPI\factor\utils.py 中添加了before_quarter_lastday函数 为了获得指定日期下上一个季末数据的日期

- [MODIFY] 由于接口的变化，修改了以下内容：
    - DataAPI\read\index_contents.py 中的 import finkit.datetime_utils.fetch as fetch 改成 import finkit.datetime_utils.utils as utils
    - DataAPI\read\index_contents.py 中的 get_A_contents函数：
        fetch.get_nearest_trading_day_before(date) 改为 utils.get_nearest_trading_day(date=date, self_included=True)

- [DEV] 开发了DataAPI\write\factor.py 中的update_factor_data函数 用于将计算好的factor写入csv文件。


## 2017-12-28

- [DEV] 开发了DataAPI\factor\calculate_factors.py中的calculate_VALUE函数，用于计算VALUE，测试通过。

- [DEV] 开发了DataAPI\load\factor.py中的load_single_factor_on_single_  day函数，用于读取indicator的值，并据此计算出factor，测试通过。

- [DEV] 在DataAPI\factor\calculate_factors.py的header中加入了对因子计算的通用方法的描述

- [DEBUG] 纠正之前在统计标准化时包括了极端值，正确的做法是基于非极端值和非缺失值求出的均值和标准差进行标准化。

- [MODIFY] 重修修改了factor的schema 将‘element’修改为‘context’；在‘explanation’中加入对该因子计算方法的简单描述

- [MODIFY] 精简了 DataAPI\read\indicator.py 中的get_secs_indicator函数

- [DEV] 开发了 DataAPI\factor\config.py 用于储存2个全局字典FACTOR_PROCESSING_MAP和FACTOR2CHS

- [DEV] 在DataAPI\factor下，将原有的VALUE_processing包拆分成 utils和calculate_factors，前者用于储存mark_
missing，winsorize，standardize等标准化函数，后者用于储存计算不同factor的函数

- [MODIFY] 将winsorize_outlier，standardize_data重命名为winsorize，standardize


## 2017-12-27

- [DEVing] 正在开发 DataAPI\factor\DataProceesing.py中VALUE_processing函数，用于处理VALUE的一些特殊处理

- [DEVing] 正在开发 DataAPI\load\factor.py中load_single_factor_on_single_day函数，用于处理读取indicator的值，并计算和处理factor

- [DEV] 开发了DataAPI\factor\DataProceesing.py中的mark_missing，winsorize_outlier，standardize_data等通用函数，分别用于对数据进行缺失值分离、异常值winsorize、统计标准化


## 2017-12-22

- [DEBUG] 修改 DataAPI/load/__init__.py ，加入了对indicator相关内容的导入

- [DEV] 开发 devkit/io_itils/file_utils.py 中的 mkdir()，用于在指定路径下创建文件夹


## 2017-12-21

- [DEV] 开发了DataAPI/read/indicator中的 get_secs_indicator()

- [DEV] 开发了DataAPI/write/indicator中的update_indicator_data函数

- [DEV] 开发了DataAPI/load/indicator中的load_indicator_data_from_wind函数

- [DEV] 开发了finkit/datetime_utils/fetch中的get_nearest_trading_day_before

- [MODIFY] 修改了DataAPI/read/index_contents中的get_A_contents函数

- [DEBUG] 校正了finkit/datetime_utils/fetch：
    get_trading_days函数定义了两次 将第二个get_trading_days函数修改成weekly_and_monthly_last_trading_days函数


## 2017-12-20

- [MODIFY] 修改 db/indicator/schema 中的字段 "财务报表数据" -> "财报数据"

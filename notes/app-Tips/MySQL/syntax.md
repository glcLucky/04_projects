# 正则表达式

1. 正则表达式与LIKE的区别

- LIKE和REGEXP的不同在于， LIKE匹配整个串而REGEXP匹配子串。
- LIKE匹配**整个列**。如果被匹配的文本在列值中出现， LIKE将不会找到它，相应的行也不被返回（除非使用通配符）。而REGEXP在**列值内**进行匹配，如果被匹配的文本在列值中出现， REGEXP将会找到它，相应的行将被返回。这是一个非常重要的差别

2. syntax

    SELECT * FROM products WHERE prod_name REGEXP '^[0-9\\.]

3. 不区分大小写
- MySQL中的正则表达式匹配默认不区分大小写
- 为区分大小写，可使用BINARY关键字，如：

    WHERE prod_name REGEXPBINARY 'JetPack .000'

4. 
- ```or```  搜索多个串之一 如：
   
    WHERE  prod_name REGEXP '1000|2000|3000'


- ```[]``` 匹配几个字符之一 注意是单个字符 字符串不可以

    WHERE prod_name REGEXP '^[bir|det]'

正则表达式并不是找出bir和det开头的 而是找出以b,i,r,|,d,e,t开头的 应当用```'^(bir|det)'```

- 用**\\** 匹配特殊字符 比如匹配`.` 可以用REGEXP '\\.' 

5. 匹配字符类 （character class）
[:alnum:] 任意字母和数字（同[a-zA-Z0-9]）
[:alpha:] 任意字符（同[a-zA-Z]）
[:blank:] 空格和制表（同[\\t]）
[:cntrl:] ASCII控制字符（ASCII 0到31和127）
[:digit:] 任意数字（同[0-9]）
[:graph:] 与[:print:]相同，但不包括空格
[:lower:] 任意小写字母（同[a-z]）
[:print:] 任意可打印字符
[:punct:] 既不在[:alnum:]又不在[:cntrl:]中的任意字符
[:space:] 包括空格在内的任意空白字符（同[\\f\\n\\r\\t\\v]）
[:upper:] 任意大写字母（同[A-Z]）
[:xdigit:] 任意十六进制数字（同[a-fA-F0-9]）

6. 匹配多个实例

        * 0个或多个匹配
        + 1个或多个匹配（等于{1,}）
        ? 0个或1个匹配（等于{0,1}）
        {n} 指定数目的匹配
        {n,} 不少于指定数目的匹配
        {n,m} 匹配数目的范围（m不超过255）

注意都是匹配前面的字符 比如`'hd?'` 表示可以出现一个d或者不出现d

7. 定位符

    ^ 文本的开始
    $ 文本的结尾
    [[:<:]] 词的开始
    [[:>:]] 词的结尾

注：^的双重用途 ^有两种用法。在集合中（用[和]定义），用它来否定该集合，否则，用来指串的开始处。

8. 简单的正则表达式测试 
可以在不使用数据库表的情况下用SELECT来测试正则表达式。REGEXP检查总是返回0（没有匹配）或1（匹配）。可以用带文字串的REGEXP来测试表达式，并试验它们。相应的语法如下：

    SELECT 'HELLO' REGEXP '[0-9]'


# 字段计算

1. 必要性 
可在SQL语句内完成的许多转换和格式化工作都可以直接在客户机应用程序内完成。但一般来说，在数据库服务器上完成这些操作比在客户机中完
成要快得多，因为DBMS是设计来快速有效地完成这种处理的。

2. 字符串函数

    
    concat() 拼接
    Left() 返回串左边的字符
    Length() 返回串的长度
    Locate() 找出串的一个子串
    Lower() 将串转换为小写
    LTrim() 去掉串左边的空格
    Right() 返回串右边的字符
    RTrim() 去掉串右边的空格
    Soundex() 返回串的SOUNDEX值
    SubString() 返回子串的字符
    Upper() 将串转换为大写

3. 日期函数

    AddDate() 增加一个日期（天、周等）
    AddTime() 增加一个时间（时、分等）
    CurDate() 返回当前日期
    CurTime() 返回当前时间
    Date() 返回日期时间的日期部分
    DateDiff() 计算两个日期之差
    Date_Add() 高度灵活的日期运算函数
    Date_Format() 返回一个格式化的日期或时间串
    Day() 返回一个日期的天数部分
    DayOfWeek() 对于一个日期，返回对应的星期几
    Hour() 返回一个时间的小时部分
    Minute() 返回一个时间的分钟部分
    Month() 返回一个日期的月份部分
    Now() 返回当前日期和时间
    Second() 返回一个时间的秒部分
    Time() 返回一个日期时间的时间部分
    Year() 返回一个日期的年份部分

4. 数值处理函数

    Abs() 返回一个数的绝对值
    Cos() 返回一个角度的余弦
    Exp() 返回一个数的指数值
    Mod() 返回除操作的余数
    Pi() 返回圆周率
    Rand() 返回一个随机数
    Sin() 返回一个角度的正弦
    Sqrt() 返回一个数的平方根
    Tan() 返回一个角度的正切

5. 聚集函数（ aggregate function）

- 必要性：返回实际表数据是对时间和处理资源的一种浪费（更不用说带宽了）。重复一遍，实际想要的是汇总信息
这些函数是高效设计的，它们返回结果一般比你在自己的客户机应用程序中计算要快得多

- 常见的汇总函数
    AVG() 返回某列的平均值 AVG()函数忽略列值为NULL的行。
    COUNT() 返回某列的行数 使用COUNT(\*)对表中行的数目进行计数 不管表列中包含的是空值（NULL）还是非空值。
            使用COUNT(column)对特定列中具有值的行进行计数，忽略NULL值。
    MAX() 返回某列的最大值
    MIN() 返回某列的最小值
    SUM() 返回某列值之和

- 聚集范围
默认为ALL 即对所有记录聚集 如果只针对不同值则可加入关键词 DISTINCT
SELECT DISTINCT vend_id FROM products ：选择所有不重复的vend_id
SELECT DISTINCT vend_id, prod_price  FROM products ：选择所有vend_id和prod_price组合不重复的记录
SELECT AVG(DISTINCT prod_price)  FROM products: 计算不重复的price的平均

# 数据分组

1. GROUP BY

- GROUP BY子句中列出的每个列都必须是检索列或有效的表达式（但不能是聚集函数）。如果在SELECT中使用表达式，则必须在GROUP BY子句中指定相同的表达式。不能使用别名

- 除聚集计算语句外， SELECT语句中的每个列都必须在GROUP BY子句中给出

- 如果分组列中具有NULL值，则NULL将作为一个分组返回。如果列中有多行NULL值，它们将分为一组。

- GROUP BY子句必须出现在WHERE子句之后， ORDER BY子句之前。

- 使用WITH ROLLUP关键字，可以得到每个分组以及每个分组汇总级别（针对每个分组）的值,即总计

- 一般在使用GROUP BY子句时，应该也给出ORDER BY子句。这是保证数据正确排序的唯一方法。千万不要仅依赖GROUP BY排序数据。

2. HAVING & WHERE
- HAVING叫做'过滤分组'，HAVING非常类似于WHERE，唯一的差别是WHERE过滤**行**，而HAVING过滤**分组** 
- HAVING支持所有WHERE操作符 
- 这里有另一种理解方法，WHERE在数据分组前进行过滤， HAVING在数据分组后进行过滤。这是一个重要的区别， WHERE排除的行不包括在分组中。这可能会改变计算值，从而影响HAVING子句中基于这些值过滤掉的分组

3. SELECT子句顺序
    子句          说明                                          是否必须要使用
    SELECT        要返回的列或表达式                                 是
    FROM          从中检索数据的表                               仅在从表选择数据时使用
    WHERE         行级过滤                                          否
    GROUP BY      分组说明                                      仅在按组计算聚集时使用
    HAVING        组级过滤                                          否
    ORDER BY      输出排序顺序                                       否
    LIMIT         要检索的行数                                        否


# 连接

1. 外键
    外键为某个表中的一列，它包含另一个表的主键值，定义了两个表之间的关系

2. 可伸缩性（scale）
    能够适应不断增加的工作量而不失败。设计良好的数据库或应用程序称之为可伸缩性好（ scale well） 

3. 指定别名
    表别名只在查询执行中使用。与列别名不一样，表别名不返回到客户机

# 组合

1. UNION从查询结果集中自动去除了重复的行 这是UNION的默认行为，但是如果需要，可以改变它。事实上，如果
想返回所有匹配行，可使用UNION ALL而不是UNION
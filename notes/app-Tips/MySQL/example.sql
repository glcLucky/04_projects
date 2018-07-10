# 创建表
CREATE TABLE test1 
(
    id CHAR(3) NOT NULL,
    result CHAR(4) NOT NULL,
    channel CHAR(20) NOT NULL,
    PRIMARY KEY  (id, channel, result)
) ENGINE=InnoDB;

# 插入数据
INSERT INTO test1(
    id,
    result,
    channel)
VALUES
    ('1', 'SUCC', 'PC'),
    ('2', 'SUCC', 'MOBILE'),
    ('3', 'FAIL', 'PC'),
    ('2', 'FAIL', 'MOBILE'),
    ('1', 'SUCC', 'IPAD')
    ;

# 求比例
SELECT channel,
       SUM(CASE WHEN result = 'FAIL' THEN 1 ELSE 0 END) AS FAIL,
       count(*) AS N,
       SUM(CASE WHEN result = 'FAIL' THEN 1 ELSE 0 END) / count(*) AS PCT

FROM test1
GROUP BY channel
;

# FROM 来源于一个SELECT语句 要加别名
SELECT (*)
FROM
(
SELECT a.order_num, b.prod_id
FROM orders as a
LEFT OUTER JOIN orderitems as b
on a.order_num=b.order_num
) AS C

WHERE C.prod_id='ANV01' and C.order_num='20005'
;


# -*- coding: utf-8 -*-


"""
fetch.py

从MySQL数据库中获取需要的数据集
"""
from .. config import (
    USER,
    PASSWORD,
)

# 连接数据库
conn = dk.MySQLProxy()
conn.connect(USER, PASSWORD, "indicator")


def get_close_by_year()
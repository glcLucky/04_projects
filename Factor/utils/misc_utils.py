# -*- coding: utf-8 -*-


def options2str(options):
    """
    将字典转化成自字符串 用分号连接
    e.g. {'name':'gui','sex':,'male'} 转变成 "name=gui;sex=male"
    """

    return ";".join("{}={}".format(key, val) for key, val in options.items() if val is not None)

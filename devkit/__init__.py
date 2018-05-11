# -*- coding: utf-8 -*-

"""
devkit

个人使用的开发工具包

@author: Wu Yudi
@email: jasper.wuyd@gmail.com
@date: 2017.09.27
"""


from . config import _DEPENDENCIES

for pkg in _DEPENDENCIES:
    try:
        __import__(pkg)
    except:
        print("WARNING: Fail to import {}!".format(pkg))

from . import (
    api,
    code_utils,
    data_utils,
    io_utils,
)

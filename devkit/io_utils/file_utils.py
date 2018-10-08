# -*- coding: utf-8 -*-

"""
file_utils.py

与文件相关的IO函数库

@author: Jasper Gui
@email: jasper.gui@outlook.com
@date: 2017.12.11

---------------

FUNCTION LIST:
- validate_file(filepath)
"""

import os


def validate_file(filepath):
    if os.path.exists(filepath):
        return True
    else:
        raise ValueError("{} not found!".format(filepath))

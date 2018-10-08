# -*- coding: utf-8 -*-

"""
db_utils.py

数据库工具函数

@author: Jasper Gui
@email: jasper.gui@outlook.com
@date: 2018.03.13

-------------------

FUNCTION LIST:
- open_db_folder(db="")
"""

import subprocess

from devkit.api import Logger

from .. config import DB_PATH, DB_PATH_LIB


def open_db_folder(db=""):
    if not db:
        path = DB_PATH
    elif db in DB_PATH_LIB:
        path = DB_PATH_LIB[db]
    else:
        Logger.error("db not found: {}".format(db))

    subprocess.Popen(r'explorer "{}"'.format(path))

# -*- coding: utf-8 -*-

"""
path.py

路径配置文件

@author: Jasper Gui
@email: jasper.gui@outlook.com
@date: 2017.12.08

-----------------

FUNCTION LIST:
- get_db_path()
- set_db_path(path)
- reset_db_path()
"""

import os
import json

from devkit.api import json2dict
from . db_names import DB_NAMES


# ~/<module>/
_FOLDER = os.path.realpath(__file__)
for _ in range(2):
    _FOLDER = os.path.split(_FOLDER)[0]

# ~/
_OUTER_FOLDER = os.path.split(_FOLDER)[0]


# load preference file, refresh DB_PATH
PREFERENCE_FILE = os.path.join(_FOLDER, "preferences.json")
with open(PREFERENCE_FILE, 'r', encoding="utf-8") as _f:
    PREFERENCE = json.load(_f)

DB_PATH = PREFERENCE["DB_PATH"]
if not DB_PATH:
    DB_PATH = os.path.join(_OUTER_FOLDER, "db")
    print("WARNING: Empty DB_PATH, automatically redirect to: {}".format(DB_PATH))
if not os.path.exists(DB_PATH):
    _p = DB_PATH
    DB_PATH = os.path.join(_OUTER_FOLDER, "db")
    print("WARNING: DB_PATH not found at {}, automatically redirect to: {}".format(_p, DB_PATH))

DB_PATH_LIB = {db: os.path.join(DB_PATH, db) for db in DB_NAMES}

SERVER = "user='root', password='123888'"

# def get_db_path():
#     print("Current database path is: {}".format(DB_PATH))


# def set_db_path(path):
#     global PREFERENCE, DB_PATH
#     PREFERENCE["DB_FOLDER"] = DB_PATH = path
#     devkit.api.dict2json(PREFERENCE, PREFERENCE_FILE, log=False)
#     devkit.api.Logger.info("DB_FOLDER is changed to {}".format(path))


# def reset_db_path():
#     global PREFERENCE, DB_PATH
#     PREFERENCE["DB_FOLDER"] = ""
#     DB_PATH = os.path.join(_OUTER_FOLDER, "projects")
#     devkit.api.Logger.info("DB_FOLDER is changed to {}".format(DB_PATH))
#     devkit.api.dict2json(PREFERENCE, PREFERENCE_FILE, log=False)

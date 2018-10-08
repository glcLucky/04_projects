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


# ~/<module>/
_FOLDER = os.path.realpath(__file__)
for _ in range(2):
    _FOLDER = os.path.split(_FOLDER)[0]


# load preference file, refresh DB_PATH
PREFERENCE_FILE = os.path.join(_FOLDER, "preferences.json")

with open(PREFERENCE_FILE, 'r', encoding="utf-8") as _f:
    PREFERENCE = json.load(_f)

PROJECT_PATH = PREFERENCE["PROJECT_PATH"]
USER = PREFERENCE['USER']
PASSWORD = PREFERENCE['PASSWORD']
SCHEMA_PATH = os.path.join(PROJECT_PATH, "schema")
PROJECT_FILES_PATH = PREFERENCE['PROJECT_FILES']

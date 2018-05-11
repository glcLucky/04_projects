SCHEMA
=======

**io.py**

- get_schema(db_name):

    获得某个数据库schema的相关信息

    @db_name (int): 数据库名称
    @return dict of schema


- show_dbs_composition(db_names):

    展示某个数据的构成

    @db_names (int): 数据库名称


- show_db_info(db_name):

    打印指定数据库的schema相关信息

    @db_names (int): 数据库名称


---

**update_schema.py**

- update_schema(db_name, sub_name):

    更新schema相关的begin date，end date, last update 适用于非factor_return相关的数据库

    @db_name (str): db的名称 eg. FACTOR 排除factor_return
    @sub_name (str): db中各子数据库的名称 eg. VALUE GROWTH


- update_factor_return_schema(factor):

    更新factor_return的schema相关的begin date，end date, last update

    @factor (str): factor的名称




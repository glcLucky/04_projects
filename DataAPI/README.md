DataAPI
=======

---

自用数据库管理工具

@author: Jasper Gui
@email: jasper.gui@outlook.com

---

## 代码架构说明
================

### Notations

- DB_FOLDER
    - 本地存储数据的顶层路径，可通过 ./preference.json 自行配置

- db
    - 实际数据库，如 index_contents, industry, indicator等
    - 在 config/db_names 中有所有数据库的名字列表
    - 在 DB_PATH 下以文件夹形式存在

- table
    - 数据库中的表，也指非sql形式存储的文件，某种意义上等于子数据库

- schema
    - 数据库信息，存储格式为json，但不带后缀，键为表名，内容为该表的一些信息
    - 存储于对应 db 文件夹内

### DataAPI.read

读取数据库的相关API。

### DataAPI.load

从数据源载入数据的相关API，目前以 Wind 为主要数据源。

### DataAPI.write

写入数据库的相关API。

---

## 数据库架构说明
================

每层有schema文件说明相关信息。

数据库底层采用csv/json等文件格式存储，或sqlite架构。

---

## License

`Apache 2.0`

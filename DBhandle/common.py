# 用于连接数据库等操作

import MySQLdb
import os
import time

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.types import NVARCHAR



# 使用环境变量获得数据库。兼容开发模式可docker模式。
MYSQL_HOST = os.environ.get('MYSQL_HOST') if (os.environ.get('MYSQL_HOST') != None) else "192.168.1.102"
MYSQL_USER = os.environ.get('MYSQL_USER') if (os.environ.get('MYSQL_USER') != None) else "root"
MYSQL_PWD = os.environ.get('MYSQL_PWD') if (os.environ.get('MYSQL_PWD') != None) else "Bocdc123"
MYSQL_DB = os.environ.get('MYSQL_DB') if (os.environ.get('MYSQL_DB') != None) else "stock_data"

print("MYSQL_HOST :", MYSQL_HOST, ",MYSQL_USER :", MYSQL_USER, ",MYSQL_DB :", MYSQL_DB)
MYSQL_CONN_URL = "mysql+mysqldb://" + MYSQL_USER + ":" + MYSQL_PWD + "@" + MYSQL_HOST + ":3306/" + MYSQL_DB + "?charset=utf8mb4"
print("MYSQL_CONN_URL :", MYSQL_CONN_URL)


# 通过MySQLdb数据库链接 engine。
def conn(DB = MYSQL_DB):
    try:
        db = MySQLdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PWD, DB, charset="utf8")
        # db.autocommit = True
    except Exception as e:
        print("conn error :", e)
        
    db.autocommit(on=True)
    return db.cursor()


# 插入数据
def insert(sql, params=()):
    with conn() as db:
        print("insert sql:" + sql)
        try:
            db.execute(sql, params)
        except  Exception as e:
            print("error :", e)
            insertLog(message="Insert failed", level=5, flag="ERROR")


# 查询数据
def select(sql, params=()):
    with conn() as db:
        print("select sql:" + sql)
        try:
            db.execute(sql, params)
        except  Exception as e:
            print("error :", e)
            insertLog(message="Select failed", level=5, flag="ERROR")
        result = db.fetchall()
        return pd.DataFrame(list(result))


# 计算数量
def select_count(sql, params=()):
    with conn() as db:
        print("select sql:" + sql)
        try:
            db.execute(sql, params)
        except  Exception as e:
            print("error :", e)
            insertLog(message="Select failed", level=5, flag="ERROR")
        result = db.fetchall()
        # 只有一个数组中的第一个数据
        if len(result) == 1:
            return int(result[0][0])
        else:
            return 0


# 通过sqlalchemy连接数据库
def engine_to_db(to_db):
    MYSQL_CONN_URL_NEW = "mysql+mysqldb://" + MYSQL_USER + ":" + MYSQL_PWD + "@" + MYSQL_HOST + ":3306/" + to_db + "?charset=utf8mb4"
    engine = create_engine(
        MYSQL_CONN_URL_NEW,
        encoding='utf8')#, convert_unicode=True)
    return engine


# 插入数据alchemy方法
def insertSQL(data, sheet, exist='replace'):
    engine_mysql = engine_to_db(MYSQL_DB)
    col_name_list = data.columns.tolist()
    data.to_sql(name=sheet, con=engine_mysql, schema=MYSQL_DB, if_exists=exist,
                dtype={col_name: NVARCHAR(length=255) for col_name in col_name_list}, index=False)


# 向logger数据库中写入日志
def insertLog(message="", level=1, flag="Normal"):
    datetime = time.strftime("%Y%m%d%H%M%S")
    data = [[message, level, datetime, flag]]
    columns = ['Message', 'level', 'datetime', 'type']
    df = pd.DataFrame(data,columns=columns)
    print(df)
    engine_mysql = engine_to_db(MYSQL_DB)
    col_name_list = df.columns.tolist()
    print(col_name_list)
    df.to_sql(name='logger', con=engine_mysql, schema=MYSQL_DB, if_exists='append',
                dtype={col_name: NVARCHAR(length=255) for col_name in col_name_list})#, index='code')

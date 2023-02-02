# 用于连接数据库等操作

import MySQLdb
import os
from DBhandle import common
from DBhandle import stockHandle
from getData import getAkshare


dicts = ['stock_list', 'stock_price']


def create_new_database():
    with MySQLdb.connect(common.MYSQL_HOST, common.MYSQL_USER, common.MYSQL_PWD, "mysql", charset="utf8") as db:
        try:
            create_sql = " CREATE DATABASE IF NOT EXISTS %s CHARACTER SET utf8 " % common.MYSQL_DB
            print(create_sql)
            db.autocommit(on=True)
            db.cursor().execute(create_sql)
        except Exception as e:
            print("error CREATE DATABASE :", e)


def emptyTest(params=()):
    sql = "select 1"
    with common.conn() as db:
        print("empty test")
        try:
            db.execute(sql, params)
            print("########### db exists ###########")
        except  Exception as e:
            print("error :", e)
            return True

        for dict in dicts:
            sql = f"select * from {dict}"
            try:
                print("create sql:" + sql)
                db.execute(sql)
                print(f"########### sheet {dict} exists ###########")
            except Exception as e:
                print("error :", e)
                return True
    return False


def createSheets(params=()):
    sqls = ["CREATE TABLE stock_list (code VARCHAR(255) PRIMARY KEY UNIQUE, name VARCHAR(255))",#, industry SET('1','2','3'))",
           "CREATE TABLE stock_price (Id_P int)",
           "CREATE TABLE industry (Id_P int)",
           "CREATE TABLE logger (Id_P int)"]
    with common.conn() as db:
        for sql in sqls:
            try:
                print("create sql:" + sql)
                db.execute(sql, params)
                print("########### sheet created ###########")
            except Exception as e:
                print("error :", e)
    return True


# try:
if __name__ == "__main__":
    if not(emptyTest()):
        # create_new_database()
        # createSheets()
        # stockHandle.historyDateSave()
        # stockPrice = common.getStockPrice('000001')
        # print(stockPrice)
        stockHandle.updateHistoryData()
        # createSheets()
        # common.insertLog(message='create log sheet', level=3, type='CREATE')
    else:
        # createStockList()
        stockHandle.historyDateSave()
# except Exception as e:
#     print("MYSQL_DB error and create new one :", e)
#     # 检查数据库失败，

#

# createStockList()




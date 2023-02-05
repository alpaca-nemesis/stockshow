from DBhandle import common
import time
from getData.getAkshare import getHistoryStocks
from getData.getAkshare import getUpdateStockStatus
from getData.getAkshare import getStockList


# 获取股票列表
def getStockListGot(params=()):
    sql = "SELECT TABLE_NAME FROM information_schema.tables WHERE table_schema='%s' AND TABLE_NAME REGEXP '[0-9]{6}' ORDER BY TABLE_NAME" % common.MYSQL_DB
    print(sql)
    try:
        result = common.select(sql)
        common.insertLog(message="Get stock list", level=1, flag="NORMAL")
    except  Exception as e:
        print("error :", e)
    if not result.empty:
        result.columns = ['code']
    return result


# 查询特定股票的历史数据
def getStockPrice(stock, startDate='20170101', endDate=None):
    if endDate is None:
        endDate = time.strftime("%Y%m%d")
    sql = 'SELECT * FROM `%s`' % stock
    try:
        stockPrice = common.select(sql)
        common.insertLog(message="Get stock price of %s" % stock, level=1, flag="NORMAL")
    except  Exception as e:
        print("error :", e)
        common.insertLog(message="Select failed", level=5, flag="ERROR")
    # stockPrice.set_index(0, inplace=True)
    stockPrice.columns = ['date', 'openingP', 'closingP', 'maxP', 'minP', 'turnover', 'turnoverP', 'amplitude', 'fluctuation', 'fluctuationP', 'turnoverRate']
    return stockPrice


# 创建股票列表并保存到本地
def createStockList():
    stockList = getStockList()
    # stockList.set_index('code', inplace=True)
    try:
        common.insertSQL(stockList, "stock_list")
        common.insertLog(message="Create stock list", level=3, flag="NORMAL")
    except  Exception as e:
        print("error :", e)
        common.insertLog(message="Create stock list failed", level=5, flag="ERROR")


# 从数据库中获取已保存的股票列表
def getStockListAll():
    sql = 'SELECT * FROM stock_list'
    try:
        stocks = common.select(sql)
        common.insertLog(message="Get all stock saved", level=1, flag="NORMAL")
    except  Exception as e:
        print("error :", e)
        common.insertLog(message="Create stock list failed", level=5, flag="ERROR")

    stocks.set_index(0, inplace=True)
    stocks.columns = ['code', 'name']
    return stocks


# 读取历史数据并存储到本地数据库
def historyDateSave(startDate='20170101', endDate=None):
    if endDate is None:
        endDate = time.strftime("%Y%m%d")
    stocks = getStockListAll()
    # print(stocks)
    # count = 1
    stockListGot = getStockListGot()
    if stockListGot.empty:
        stockListGot = []
    else:
        stockListGot = list(stockListGot['code'])
    print(stockListGot)
    for stock in stocks['code']:
        print(stocks.loc[stocks['code'] == stock])
        if stock in stockListGot:
            continue
        stock_zh_a_hist_df = getHistoryStocks(stock, startDate, endDate)
        # print(stock_zh_a_hist_df.columns)
        try:
            common.insertSQL(stock_zh_a_hist_df, stock)
            common.insertLog(message="Save stock %s" % stock, level=3, flag="NORMAL")
        except  Exception as e:
            print("error :", e)
            common.insertLog(message="Create stock price of %s failed" % stock, level=5, flag="ERROR")

        # time.sleep(0.01)
        # print(stock_zh_a_hist_df)
        # if count == 5:
        #     time.sleep(0.1)
        #     count = 0
        # count += 1


# 获取每日数据并更新至列表
def updateHistoryData(date=None):
    spotData = getUpdateStockStatus(date=date)
    stocks = getStockListAll()
    print("update history stock data. Date:", date)
    for stock in stocks['code']:
        # print(stocks.loc[stocks['code'] == stock])

        toWrite = spotData.loc[spotData['code'] == stock]
        toWrite = toWrite.drop('code', axis=1)
        # print(toWrite)
        try:
            common.insertSQL(toWrite, stock, exist='append')
        except  Exception as e:
            print("error :", e)
            common.insertLog(message="refresh stock price of %s failed" % stock, level=5, flag="ERROR")

        time.sleep(0.05)
    common.insertLog(message="All stock price refresh", level=3, flag="NORMAL")


if __name__ == "__main__":
    getStockPrice('000001')



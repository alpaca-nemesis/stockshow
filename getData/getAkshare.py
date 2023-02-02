#用于获取数据

import pandas as pd
import akshare as ak
import re
import numpy as np
import datetime, time

column_dick = {
    '代码': 'code',
    '日期': 'date',
    '名称': 'name',
    '最新价': 'closingP',
    '今开': 'openingP',
    '昨收': 'yesEndP',
    '量比': 'volumeRate',
    '市盈率-动态': 'PERate',
    '市净率': 'PBRate',
    '总市值': 'totalMV',
    '流通市值': 'currentMV',
    '开盘': 'openingP',
    '收盘': 'closingP',
    '最高': 'maxP',
    '最低': 'minP',
    '成交量': 'turnover',
    '成交额': 'turnoverP',
    '振幅': 'amplitude',
    '涨跌幅': 'fluctuation',
    '涨跌额': 'fluctuationP',
    '板块名称': 'name',
    '板块代码': 'code',
    '上涨家数': 'upCount',
    '下跌家数': 'downCount',
    '换手率': 'turnoverRate'
}


def columnsNormal(df):
    before = df.columns
    after = []
    for column in before:
        if column in column_dick:
            after.append(column_dick[column])
        else:
            after.append(column)
    df.columns = after
    return df

#过滤代码
# 600开头的股票是上证A股，属于大盘股
# 600开头的股票是上证A股，属于大盘股，其中6006开头的股票是最早上市的股票，
# 6016开头的股票为大盘蓝筹股；900开头的股票是上证B股；
# 000开头的股票是深证A股，001、002开头的股票也都属于深证A股，
# 其中002开头的股票是深证A股中小企业股票；
# 200开头的股票是深证B股；
# 300开头的股票是创业板股票；400开头的股票是三板市场股票。
def stock_a_filter_code(code):
    # print(code)
    # print(type(code))
    # 上证A股  # 深证A股
    if code.startswith('600') or code.startswith('6006') or code.startswith('601') or code.startswith('000') or code.startswith('001') or code.startswith('002'):
        return True
    else:
        return False

# 过滤掉 st 股票。
def stock_a_filter_st(name):
    # print(code)
    # print(type(code))
    # 上证A股  # 深证A股
    if name.find("ST") == -1 or name.find("PT") == -1:
        return True
    else:
        return False

# 过滤价格，如果没有基本上是退市了。
def stock_a_filter_price(latest_price):
    # float 在 pandas 里面判断 空。
    if np.isnan(latest_price):
        return False
    else:
        return True

# 过滤价格，如果没有基本上是退市了。
def stock_a_filter_price(latest_price):
    # float 在 pandas 里面判断 空。
    if np.isnan(latest_price):
        return False
    else:
        return True



def getStockList():
    stockList = ak.stock_zh_a_spot_em()
    print(stockList.columns)
    stockList = columnsNormal(stockList)
    stockList = stockList.loc[stockList["code"].apply(stock_a_filter_code)].loc[stockList["name"].apply(stock_a_filter_st)].loc[
        stockList["closingP"].apply(stock_a_filter_price)]
    stockList.sort_values(by=['code'], inplace=True)
    stockList.reset_index(drop=True, inplace=True)
    stockList = stockList[['code', 'name']]
    print(stockList)
    return stockList


def getIndustryMatrix():
    industryList = ak.stock_board_industry_name_em()
    print(industryList.columns)
    industryList = columnsNormal(industryList)
    industryList.sort_values(by=['code'], inplace=True)
    industryList.reset_index(drop=True, inplace=True)
    industryList = industryList[['code', 'name']]
    print(industryList)
    # for name in industryList['name']:
    #     temp = ak.stock_board_industry_cons_em(symbol=name)
    #     print(industryList.loc[industryList['name'] == name])
    #     print(temp)

    return columnsNormal(industryList)


def dateHandle(dateframe, stocks=[]):
    if (re.findall(r'\d+-\d+-\d+', dateframe)) == []:
        tmp_datetime_show = datetime.datetime.now()  # 修改成默认是当日执行 + datetime.timedelta()
        tmp_hour_int = int(tmp_datetime_show.strftime("%H"))
        if tmp_hour_int < 15 :
            # 判断如果是每天 中午 15 点之前运行，跑昨天的数据。
            tmp_datetime_show = (tmp_datetime_show + datetime.timedelta(days=-1))
        else:
            pass


def getSpotStocks(stocks=[]):
    try:
        spotStockData = ak.stock_zh_a_spot_em()
        # print(spotStockData)
    except Exception as e:
        print("error :", e)

    if stocks != []:
        spotStockData = spotStockData.loc[stocks]
    return columnsNormal(spotStockData)


def getHistoryStocks(stock, startDate = '', endDate = ''):
    stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol=stock, period="daily", start_date=startDate,
                                                end_date=endDate, adjust="")
    return columnsNormal(stock_zh_a_hist_df)


def getUpdateStockStatus(date=None, stocks=[]):
    if date == None:
        spotStockData = getSpotStocks(stocks)
    else:
        # 看日期，懒得写了
        spotStockData = getSpotStocks(stocks)
    # print(spotStockData.columns)
    spotStockData = spotStockData[['code', 'openingP', 'closingP', 'maxP', 'minP', 'turnover', 'turnoverP', 'amplitude', 'fluctuation', 'fluctuationP', 'turnoverRate']]
    datePD = pd.DataFrame({'date':[time.strftime("%Y-%m-%d")] * len(spotStockData)})
    # print(datePD)
    # print(spotStockData)
    datePD = datePD.join(spotStockData)
    # pd.merge(datePD, spotStockData, on='index')
    # print(datePD)

    return datePD


# 是否为交易日
def isTradeDay(date=None):
    if date == None:
        date = datetime.datetime.now().date()
    else:
        date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
    tool_trade_date_hist_sina_df = ak.tool_trade_date_hist_sina()
    if date in tool_trade_date_hist_sina_df.values:
        return True
    else:
        return False



if __name__ == '__main__':
    spotStocks = isTradeDay('2023-2-2')
    print(spotStocks)
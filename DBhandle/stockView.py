from DBhandle import common, stockHandle
import time


def viewStockPrice(stock, startDate='20170101', endDate=None):
    if endDate is None:
        endDate = time.strftime("%Y%m%d")
    stockPrice = stockHandle.getStockPrice(stock, startDate, endDate)
    klineColumns = ['date', 'openingP', 'closingP', 'maxP', 'minP', 'turnover', 'turnoverP']
    stockPrice = stockPrice[klineColumns]
    # print(stockPrice)
    prices = list(stockPrice.values)
    # print(type(list(prices)))
    # print(prices)
    return klineColumns, prices


if __name__ == "__main__":
    viewStockPrice('600004')

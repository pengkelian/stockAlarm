from configparser import ConfigParser

import StockModel
cp = ConfigParser()


def readStockConf():
    cp.read('stock.conf', encoding='UTF-8')
    se = cp.sections()
    res = []
    for code in se:
        stockm = StockModel.StockModel()
        name = cp.get(code,"name")
        buyPrice = cp.get(code,"buy_price")
        sellerPrice = cp.get(code,"sell_price")
        stockm.buyPrice = buyPrice
        stockm.code = code
        stockm.name = name
        stockm.sellerPrice = sellerPrice
        res.append(stockm)
    return res
if __name__ == '__main__':
    res = readStockConf()
    print(res)
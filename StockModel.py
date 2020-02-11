class StockModel:
    code = 0
    buyPrice = 0
    sellerPrice = 0
    name=""


    def __str__(self):
        return 'Vector (%s,%s, %s)' % (self.name,self.buyPrice, self.code)
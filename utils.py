import tushare
import datetime


class AIOldData:
    def ai_trading_day(self):
        """
功能1：判断自然日是否是交易日（YES：返回此自然日；NO：从此自然日依次往前推至交易日 并返回）
缺点：要计算10秒左右才出结果
        :return:
        """
        date_str = "{}-{}-{}".format(self[0:4], self[4:6], self[6:8])
        y, m, d = date_str.split("-")
        my_date = datetime.date(int(y), int(m), int(d))
        return tushare.is_holiday(datetime.date.strftime(my_date, "%Y-%m-%d"))



if __name__ == "__main__":
    ai_old_data = AIOldData
    print(ai_old_data.ai_trading_day("20191007"))
    print(ai_old_data.ai_trading_day("20191008"))
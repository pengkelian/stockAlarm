from MailQQ import sendEmail
import ConfigUtils
def get_open_price(code): #获得开盘价
    df = ts.get_realtime_quotes(code)
    open_price=df['open'][0]
    return float(open_price)
def get_price(code): #获得股票实时价格
    df = ts.get_realtime_quotes(code)
    price=df['price'][0]
    return float(price)
def cal_fluctuation(price_min_ago,cur_price): #计算股票每分钟浮动比例
    fluctuation=float((cur_price-price_min_ago)/price_min_ago)
    return fluctuation

def runTask(day=0, hour=0, min=0, second=0):
    stockConf = ConfigUtils.readStockConf()
    timeCount = {}
    now = datetime.now()  # 获取当前时间
    iter_last = now

    while True:
        # Init time
        now = datetime.now()  # 获取当前时间
        # df = ts.get_realtime_quotes(code)

        strnow = now.strftime('%Y-%m-%d %H:%M:%S')
        # First next run time
        period = timedelta(days=day, hours=hour, minutes=min, seconds=second)  # 获取时间间隔
        diff = period.seconds
        # Get system current time
        iter_now = datetime.now()
        iter_now_time = iter_now.strftime('%Y-%m-%d %H:%M:%S')
        if (iter_now-iter_last).seconds>diff:
            iter_last = iter_now
            for stockModel in stockConf:
                code = stockModel.code
                name = stockModel.name
                buyPrice = float(stockModel.buyPrice)
                sellerPrice = float(stockModel.sellerPrice)
                print("现在时间:", strnow)
                # Get every start work time
                #print("start work: %s" % iter_now_time)
                # Call task func
                cur_price=get_price(code)
                print(name,"  现在股价:",cur_price)
                if code in timeCount:
                    lastAlarmTime = timeCount[code]
                    diffsecond = (iter_now-lastAlarmTime).seconds
                    if lastAlarmTime !=None and diffsecond <3600:
                        print(name," 未到再一次提醒邮件的时间")
                        continue
                if cur_price<=buyPrice:
                #if True:
                    print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
                    print("Now: %s" % iter_now_time)
                    content = '%s 当前股价变动为：%s ,设定的买入股价为%s,推荐加仓,日期为：%s' % (name, cur_price,buyPrice,iter_now_time)#自定义提醒内容
                    sendEmail(content)#发送提醒邮件
                    print("发送邮件::",name)
                    print(content)
                    timeCount[code] = iter_now
                if cur_price>=sellerPrice:
                #if True:
                    print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
                    print("Now: %s" % iter_now_time)
                    content = '%s 当前股价变动为：%s ,推荐减仓,日期为：%s' % (name, cur_price,iter_now_time)#自定义提醒内容
                    sendEmail(content)#发送提醒邮件
                    print("发送邮件::",name)
                    print(content)
                    timeCount[code] = iter_now
                continue



import tushare as ts
from datetime import *
import time

if __name__ == '__main__':
    # open_price=get_open_price(code)
    now = datetime.now()
    while True:
        print('开始启动')
        #print(datetime.now())
        try:
            runTask(second=10)
        except Exception as e:
            print("报错了",e)

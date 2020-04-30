import re
import numpy as np
import requests
from bs4 import BeautifulSoup
import time
from retrying import retry
from MailQQ import sendEmailHtml
import ConfigUtils
from datetime import *
import time


@retry(stop_max_attempt_number=10, wait_random_max=1)
def getHTMLText(url):
    headers = {'Accept': '*/*',
               'Accept-Encoding': 'gzip, deflate, br',
               'Connection': 'keep-alive',
               'Referer': 'https://googleads.g.doubleclick.net/pagead/ads?client=ca-pub-7060171147028597&output=html&h=90&slotname=5057984058&adk=3524818333&adf=515356539&w=728&fwrn=4&fwrnh=100&lmt=1544410849&rafmt=1&guci=2.2.0.0.2.2.0.0&format=728x90&url=https%3A%2F%2Fwww.carsforsale.com%2FSearch%3FSearchTypeID%3D2%26Make%3DHyundai%26Model%3DTucson%26BodyStyle%3D%26SubBodyStyle%3D%26MinModelYear%3D%26MaxModelYear%3D%26MinPrice%3D%26MaxPrice%3D%26FromEstimatedMonthlyPayment%3D%26ToEstimatedMonthlyPayment%3D%26MaxMileage%3D%26FromFuelEconomy%3D%26Radius%3D%26ZipCode%3D%26State%3D%26City%3D%26FullStateName%3D%26Latitude%3D%26Longitude%3D%26Conditions%3D%26HideRepairable%3D%26FilterImageless%3D%26PricedVehiclesOnly%3D%26OrderBy%3DRelevance%26OrderDirection%3Ddesc%26PageResultSize%3D15%26PageNumber%3D1%26TotalRecords%3D%26FromDate%3D%26ToDate%3D%26DaysListed%3D%26SourceId%3D%26SourceExternalUserID%3D&flash=32.0.0&fwr=0&resp_fmts=3&wgl=1&dt=1544410849540&bpp=40&bdt=852&fdt=111&idt=109&shv=r20181205&cbv=r20180604&saldr=aa&abxe=1&correlator=2296237836056&frm=20&pv=2&ga_vid=1116481270.1544405414&ga_sid=1544410850&ga_hid=48480944&ga_fc=0&iag=0&icsg=2334722&dssz=22&mdo=0&mso=0&u_tz=480&u_his=9&u_java=0&u_h=768&u_w=1366&u_ah=728&u_aw=1366&u_cd=24&u_nplug=5&u_nmime=7&adx=311&ady=281&biw=1349&bih=662&scr_x=0&scr_y=0&eid=21060853%2C188690903%2C410075081&oid=3&rx=0&eae=0&fc=656&brdim=0%2C0%2C0%2C0%2C1366%2C0%2C1366%2C728%2C1366%2C662&vis=1&rsz=%7C%7CeoE%7C&abl=CS&ppjl=f&pfx=0&fu=144&bc=13&osw_key=3063821004&ifi=1&uci=1.4kzd5h15v778&fsb=1&xpc=iOJzRu6CkG&p=https%3A//www.carsforsale.com&dtd=139',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
               }
    try:
        requests.adapters.DEFAULT_RETRIES = 5
        s = requests.session()
        s.keep_alive = False
        time.sleep(np.random.random(1))
        res = requests.get(url, timeout=3, headers=headers)
        res.raise_for_status()  # 如果状态码不是200，引发HTTPError异常
        res.encoding = res.apparent_encoding
        return res.text
    except(Exception)as e:
        print(e)
        return 0

'''判断输入值是否为None'''
def isnull(s):
    if s!= None:
        return s.text
    else:
        return None

'''第二个页面的详细信息'''
def get_car_details(url):
    dict = {}
    res = getHTMLText(url)
    if res != 0:
        try:
            soup = BeautifulSoup(res, 'html.parser')
            title = soup.select(
                '#basic > div.version3-detail-header.container > div.version3-detail-header-right > div.right-container > div.title > h1')
            price = soup.findAll('p', {'class': 'price detail-title-right-tagP'})
            newcarprice = soup.findAll('div', {'class': 'new-car-price detail-title-right-tagP'})
            #上牌日期、公里数、所在地、变速箱、过户记录
            basic_message = soup.find('ul', {'class': 'row-fluid list-unstyled box-list-primary-detail'})
            # 无重大事故，火烧，水泡信息
            three_type_message = soup.find('div', {'class': 'report-danger'})
            #二手车平台检测后给出的综合的评价信息
            car_describe = soup.find('div', {'class': 'report-result-des'})
            if title is not None:
                print(title)
                dict['title'] = isnull(title[0])
                dict['price'] = isnull(price[0])
                dict['newcarprice'] = isnull(newcarprice[0])
                dict['three_type_message'] = isnull(three_type_message)
                dict['basic_message'] = isnull(basic_message)
                dict['car_describe'] = isnull(car_describe)
        except(Exception)as e:
            print(e)

    return dict

'''获取每个车的的链接'''
def get_car_box_url_list(url):
    links_list = []
    res = getHTMLText(url)
    if res != 0:
        soup = BeautifulSoup(res, 'html.parser')
        links = soup.findAll(href=re.compile('car'))
        for link in links:
            links_list.append('https://www.renrenche.com' + link.attrs['href'])
    return links_list


url_header = 'https://www.renrenche.com/bj/ershouche/ft-dd/p'
url_tail = '/?ft=dd&plog_id=9e528d4d463a966f6a50ebb470e41527&&sort=publish_time&seq=desc'

if __name__ == '__main__':
    repute = []
    start = 0
    #把第二页的先放进去，免得调入第一页
    url = url_header + str(2) + url_tail
    links_list = get_car_box_url_list(url)
    for link in links_list:
        repute.append(link)
    print("第二页加载完成，下面开始监控第一页")
    while True:
        print("启动。。。")
        url = url_header + str(1) + url_tail
        links_list = get_car_box_url_list(url)
        print("抓到的二手车数量：",len(links_list))
        iter_now = datetime.now()
        iter_now_time = iter_now.strftime('%Y-%m-%d %H:%M:%S')
        content = str(iter_now_time) + "  的上新二手车车：<br/>"
        ifsend = False
        for link in links_list:
            if link is not None and link not in repute:
                ifsend = True
                repute.append(link)
                dict = get_car_details(link)
                if dict.__contains__('title'):
                    content = content + '<br/> <a href = %s >%s    价格：%s</a>' % (link,dict['title'],dict['price'])  # 自定义提醒内容
        if ifsend:
            sendEmailHtml(content)  # 发送提醒邮件
            print("发送邮件。。。")
        time.sleep(60)

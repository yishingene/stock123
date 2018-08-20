'''
測試抓取 OTC 上櫃盤後資料

http://www.tpex.org.tw/web/stock/aftertrading/daily_close_quotes/stk_quote.php?l=zh-tw

Created on 2018年7月13日
@author: rocky.wang
'''
import time
import requests
import datetime
import csv


def fetch():

    now = datetime.datetime.now()
    dt = str(int(now.strftime('%Y')) - 1911) + now.strftime('/%m/%d') # 107/07/13 
    url = "http://www.tpex.org.tw/web/stock/aftertrading/daily_close_quotes/stk_quote_result.php?l=zh-tw&d={}&_={}".format(dt, int(time.time() * 1000))
    print(url)

    r = requests.get(url)
    js = r.json()
    print(js)
    
    dt = now.strftime('%Y/%m/%d')
    rowList = []
    for data in js["aaData"]:
        rowList.append(data)
        # 日期,成交股數,成交金額,開盤價,最高價,最低價,收盤價,漲跌價差,成交筆數,RSV,K9
        row = [dt, data[8], data[9], data[4], data[5], data[6], data[2]]

    with open("otc_{}.csv".format(now.strftime('%Y%m%d')), "w", encoding="utf-8", newline="") as f1:
        writer = csv.writer(f1)
        writer.writerows(rowList)
        


if __name__ == "__main__":
    fetch()

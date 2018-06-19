'''

Created on 2018年5月21日
@author: rocky.wang
'''
import time
import requests
import datetime

# 爬回今天盤後全部的上櫃資料
# dt = "{}/{}".format(int(datetime.datetime.now().strftime("%Y")) - 1911, datetime.datetime.now().strftime("%m/%d"))
# url = "http://www.tpex.org.tw/web/stock/aftertrading/daily_close_quotes/stk_quote_result.php?l=zh-tw&d={}&_={}".format(dt, int(time.time()*1000))
# r = requests.get(url)
# js = r.json()
# print(js)
# for aaData in js["aaData"]:
#     print(aaData)


s = requests.Session()
s.get("http://mis.twse.com.tw/stock/index.jsp")
#url = "http://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=tse_{stockId}.tw&_={time}".format(stockId=stockId, time=int(time.time()) * 1000)
# url = "http://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=otc_{stockId}.tw&_={time}".format(stockId=stockId, time=int(time.time()) * 1000)

#url = "http://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=otc_4205.tw|otc_1264.tw&_={}".format(int(time.time()) * 1000)

#url = "http://mis.twse.com.tw/stock/api/getStockInfo.jsp?json=1&delay=0&_={}&ex_ch=tse_1101.tw|tse_1232.tw".format(int(time.time()) * 1000)
url = "http://mis.twse.com.tw/stock/api/getStockInfo.jsp?json=1&delay=0&_={}&ex_ch=tse_1101.tw||tse_1232.tw".format(int(time.time()*1000)+1000000)

print("\nGET %s" %(url))
r = s.get(url)
print("[" + r.text.strip() + "]")
# print(r.json())

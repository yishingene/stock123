'''
抓取個股配股配息資料

Created on 2018年2月18日
@author: rocky.wang
'''
import requests, json, time
from bs4 import BeautifulSoup


def fetch(price, sid):
    
    url = "https://goodinfo.tw/StockInfo/StockDividendSchedule.asp?STOCK_ID=" + sid
    
#     headers = { 'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36',
#                     'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#                 }
    
    headers = {"User-Agent" : "Chrome/31.0.1650.63"}
    
    r = requests.get(url, headers=headers)
    r.encoding = 'UTF-8'
    
    soup = BeautifulSoup(r.text, "html.parser")
    
    tb = soup.find("table", {"class": "solid_1_padding_4_3_tbl"})
    
    elem = tb.findAll("tr", {"height": "23px"})
    
    cnt = 0
    num = 0
    fiveMoney = 0
    for tr in elem:
        tds = tr.findAll("td")
        m = float(tds[10].text)
        s = float(tds[13].text)
        num += 1
        if num <= 5:
            fiveMoney += m
            
        x, y, z = calRate(price, m, s)
        print("%s年  配息 %.2f\t   配股 %.2f      殖利率: %5s\t%5s\t%5s" %(tds[1].text, float(tds[10].text), float(tds[13].text), x, y, z))
        cnt += 1
        if cnt >=10:
            break
        
    xxx = round(fiveMoney/5/price*100, 2)
    print("\n近五年平均配息 {}，平均現金殖利率 {} %，便宜價格 {}".format(round(fiveMoney/5, 2), xxx, round(fiveMoney/5, 2)*16))

def fetchStock(stockId):

    s = requests.Session()
    s.get("http://mis.twse.com.tw/stock/index.jsp")
    url = "http://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=tse_{stockId}.tw&_={time}".format(stockId=stockId, time=int(time.time()) * 1000)
#     url = "http://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=otc_{stockId}.tw&_={time}".format(stockId=stockId, time=int(time.time()) * 1000)
    print("\nGET %s" %(url))
    r = s.get(url)

    try:
        return r.json()
    except json.decoder.JSONDecodeError:
        return {'rtmessage': 'json decode error', 'rtcode': '5000'}

''' 計算殖利率 '''
def calRate(price:float, m:float, s:float):
    t = m * 1000 + s * 100 * price # 總獲利
    x = t / (price * 1000) * 100 # 總獲利 / 總成本
    
    y = (m + s) / price * 100 # 直接配息 + 配股進行計算
    z = m / price * 100 # 直接配息 + 配股進行計算
    
    return format(x, ".2f"), format(y, ".2f"), format(z, ".2f")

if __name__ == "__main__":

    sid = "6024"

    j = fetchStock(sid)
    print(j)
    
    z = j["msgArray"][0]["z"] # 現價
    
    print()
    price = float(z)
    price20 = price * 1.2
    price30 = price * 1.3
    print("%s %s 現價 %s    " %(j["msgArray"][0]["n"], j["msgArray"][0]["c"], price))
    print()
    fetch(price, sid)
    
#     xx = calRate(8, 0, 0.4)
#     print()
#     print()
#     print(xx)
    
    

        
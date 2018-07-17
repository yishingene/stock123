'''
https://goodinfo.tw/StockInfo/StockDividendSchedule.asp?STOCK_ID=9924

Created on 2018年7月17日
@author: rocky.wang
'''
import requests
from bs4 import BeautifulSoup
import re
import csv
import os
import time
import traceback
import lineTool

eachTimeToSleepWhenFetch = 10

def main():
    
#     sid = "9924"
#     rowList = fetch(sid)
#     with open("stockDividendSchedule_{}.csv".format(sid), "w", newline="", encoding="utf-8") as f1:
#         csv.writer(f1).writerows(rowList)
        
    # 用來比對已經執行過的，不再重新執行
    existList = []
    for name in os.listdir():
        if name.startswith("stockDividendSchedule_"):
            sid = name.split(".")[0].split("_")[1]
            existList.append(sid)
    
    cnt = 0
    for name in os.listdir("../data"):
        if name == "t00.csv":
            continue
        
        sid = name.split(".")[0]

        if sid in existList:
            continue
        
#         if sid.startswith("0"):
#             print("先跳過", sid)
#             continue
        
        cnt += 1 
        try:
            rowList = fetch(sid)
        except:
            traceback.print_exc()
            print("sleep 60 seconds and try again...")
            time.sleep(60)
            rowList = fetch(sid)
        
        with open("stockDividendSchedule_{}.csv".format(sid), "w", newline="", encoding="utf-8") as f1:
            csv.writer(f1).writerows(rowList)
     
        time.sleep(eachTimeToSleepWhenFetch)
        

def fetch(sid):
    
    rowList = [['盈餘所屬年度', '股利發放年度', '股東會日期', '除息交易日', '除息參考價(元)', '除權交易日', '除權參考價(元)', '現金股利發放日', '現金股利盈餘', '現金股利公積', '現金股利合計', '股票股利盈餘', '股票股利公積', '股票股利合計', '股利合計', '發放年度平均股價', '年均殖利率(%)']]
    
    url = "https://goodinfo.tw/StockInfo/StockDividendSchedule.asp?STOCK_ID={}".format(sid)
    print(url)
    headers = {
        "User-Agent" : "Chrome/31.0.1650.63"
    }
    r = requests.get(url, headers=headers)
    r.encoding = "utf-8"
    
    if "查無除權息日程訊息" in r.text:
        return rowList

    if "您的瀏覽量異常, 已影響網站速度" in r.text:
        lineTool.lineNotify(os.environ["LINE_TEST_TOKEN"], "fetchStockDividendSchedule too fast to be blocked")

    soup = BeautifulSoup(r.text, "html.parser")
    
    trs = soup.find("table", {"class": "solid_1_padding_3_3_tbl"}).findAll("tr", id=re.compile("^row"))
    for tr in trs:
        row = []
        for td in tr.findAll("td"):
            row.append(td.text)
            
        rowList.append(row)

    return rowList


if __name__ == "__main__":
    try:
        main()
    except:
        traceback.print_exc()
        lineTool.lineNotify(os.environ["LINE_TEST_TOKEN"], "fetchStockDividendSchedule error")
    

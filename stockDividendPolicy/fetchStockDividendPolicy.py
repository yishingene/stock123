# -*- coding:utf-8 -*-

'''
https://goodinfo.tw/StockInfo/StockDividendPolicy.asp?STOCK_ID=2884

Created on 2018年9月3日
@author: rocky.wang
'''
import requests
from bs4 import BeautifulSoup
import csv
import os
import time
import traceback
import lineTool

sleepSeconds = 8

def main1():

    sid = "2884"
    rowList = fetch(sid)
    with open("stockDividendPolicy_{}.csv".format(sid), "w", newline="", encoding="utf-8") as f1:
        csv.writer(f1).writerows(rowList)

def main():
    
    # 用來比對已經執行過的，不再重新執行
    existList = []
    for name in os.listdir():
        if name.startswith("stockDividendPolicy_"):
            sid = name.split(".")[0].split("_")[1]
            existList.append(sid)
    
    cnt = 0
    for name in os.listdir("../data"):
        if name == "t00.csv":
            continue
        
        sid = name.split(".")[0]

        if sid in existList:
            continue
        
        if sid.startswith("0"):
            continue
        
        cnt += 1 
        try:
            rowList = fetch(sid)
        # 我用來代表被 block 掉了
        except EOFError as e:
            raise e
        except:
            traceback.print_exc()
            print("sleep 60 seconds and try again...")
            time.sleep(60)
            rowList = fetch(sid)
        
        with open("stockDividendPolicy_{}.csv".format(sid), "w", newline="", encoding="utf-8") as f1:
            csv.writer(f1).writerows(rowList)
     
        time.sleep(sleepSeconds)
        

def fetch(sid):
    
    rowList = [['盈餘發放年度', '現金股利盈餘', '現金股利公積', '現金股利合計', '股票股利盈餘', '股票股利公積', '股票股利合計', '股利合計', '股利總計現金(億)', '股利總計股票(千張)', '董監酬勞合計(百萬)', '董監酬勞合計佔淨利(%)', '員工紅利現金(億)', '員工紅利股票(千張)', '股價年度', '股價統計(元)最高', '股價統計(元)最低', '股價統計(元)年均', '年均殖利率(%)現金', '年均殖利率(%)股票', '年均殖利率(%)合計', '盈餘年度', 'EPS(元)', '盈餘分配率(%)配息', '盈餘分配率(%)配股', '盈餘分配率(%)合計']]
    
    url = "https://goodinfo.tw/StockInfo/stockDividendPolicy.asp?STOCK_ID={}".format(sid)
    print(url)
    headers = {
        "User-Agent" : "Chrome/31.0.1650.63"
    }
    r = requests.get(url, headers=headers)
    r.encoding = "utf-8"
    
    if "查無除權息日程訊息" in r.text:
        return rowList

    if "您的瀏覽量異常, 已影響網站速度" in r.text:
        lineTool.lineNotify(os.environ["LINE_TEST_TOKEN"], "fetchstockDividendPolicy too fast to be blocked")
        raise EOFError()

    soup = BeautifulSoup(r.text, "html.parser")
    trs = soup.findAll("table", {"class": "solid_1_padding_4_0_tbl"})[1].findAll("tr")
    for tr in trs:
        
        if not tr.has_attr("onmouseover"):
            continue
        
        row = []
        for td in tr.findAll("td"):
            row.append(td.text)
            
        rowList.append(row)

    return rowList


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        lineTool.lineNotify(os.environ["LINE_TEST_TOKEN"], e)
    

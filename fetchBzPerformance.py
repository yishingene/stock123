'''
抓取全部的 bzPerformance

Created on 2018年4月23日
@author: rocky.wang
'''
import requests
from bs4 import BeautifulSoup
import re
import csv
import os
import time
import lineTool
import datetime


def main():
    
    # 用來比對已經執行過的，不再重新執行
    existNameList = []
    for name in os.listdir("data_bzPerformance"):
        existNameList.append(name)
    
    for name in os.listdir("data"):
        if name == "t00.csv":
            continue
        
        if name in existNameList:
            print("已有資料，不再重新抓取", name)
            continue
        
        stockId = name.split(".")[0]
        
        fetchStockBzPerformanceWithRetry(stockId)

        print("sleep 20 seconds then start...")
        time.sleep(20)
        
        
def fetchStockBzPerformanceWithRetry(stockId, retry=2):
    
    try:
        fetchStockBzPerformance(stockId)
    except Exception as e:
        print("Error Occur, retry ", e)
        # 如果是瀏覽量異常，再試也沒意義了
        if str(e) == "您的瀏覽量異常, 已影響網站速度，我被抓包了":
            raise e
        
        time.sleep(10)
        retry -= 1
        if retry > 0:
            fetchStockBzPerformanceWithRetry(stockId, retry)
        else:
            raise Exception("重試超過三次失敗")

def fetchStockBzPerformance(stockId):
    print("\n{} 執行時間 {}".format(stockId, datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')))
    
    url = "https://goodinfo.tw/StockInfo/StockBzPerformance.asp?STOCK_ID={}".format(stockId)
    resp = requests.get(url, headers={"User-Agent" : "Chrome/31.0.1650.63"})
    resp.encoding = "utf-8"
    
    if "您的瀏覽量異常, 已影響網站速度" in resp.text:
        raise Exception("您的瀏覽量異常, 已影響網站速度，我被抓包了")
    
    soup = BeautifulSoup(resp.text, "html.parser")
    table = soup.find("table", {"class": "solid_1_padding_3_0_tbl", "style": "font-size:10pt;line-height:16px;"})
    
    if table == None:
        print("no data for", stockId)
        with open("data_bzPerformance/{}.csv".format(stockId), "w", newline="", encoding="utf-8") as f1:
            writer = csv.writer(f1)
            writer.writerows([])
        return
    
    trList = table.findAll("tr", id=re.compile("^row"))

    rowList = []
    for tr in trList:
        row = []
        for td in tr.findAll("td"):
            text = td.text.strip().replace(",", "")
            row.append(text)
        rowList.append(row)
    
    with open("data_bzPerformance/{}.csv".format(stockId), "w", newline="", encoding="utf-8") as f1:
        writer = csv.writer(f1)
        writer.writerows(rowList)
        

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        lineTool.lineNotify(os.environ["LINE_TEST_TOKEN"], e)

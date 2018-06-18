'''
抓取所有的
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
    for name in os.listdir("data_assetsStatus"):
        existNameList.append(name)
    
    for name in os.listdir("data"):
        if name == "t00.csv":
            continue
        
        if name in existNameList:
            print("已有資料，不再重新抓取", name)
            continue
        
        stockId = name.split(".")[0]
        
#         if stockId.startswith("0"):
#             print("0 開頭我先跳過")
#             continue
        
        fetchStockAssetsStatusWithRetry(stockId)

        print("sleep x seconds then start...")
        time.sleep(5)
        
        
def fetchStockAssetsStatusWithRetry(stockId, retry=2):
    
    try:
        fetchStockAssetsStatus(stockId)
    except Exception as e:
        print("Error Occur, retry ", e)
        # 如果是瀏覽量異常，再試也沒意義了
        if str(e) == "您的瀏覽量異常, 已影響網站速度，我被抓包了":
            raise e
        
        time.sleep(10)
        retry -= 1
        if retry > 0:
            fetchStockAssetsStatusWithRetry(stockId, retry)
        else:
            raise Exception("重試超過三次失敗")

def fetchStockAssetsStatus(stockId):

    print("\n{} 執行時間 {}".format(stockId, datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')))
    
    url = "https://goodinfo.tw/StockInfo/StockAssetsStatus.asp"    
    headers = {
        "referer": "https://goodinfo.tw/StockInfo/StockAssetsStatus.asp?STOCK_ID=1264",
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36", 
    }
    data = {
        "STOCK_ID": stockId, 
        "RPT_CAT": "M_YEAR", 
        "STEP": "DATA", 
        "SHEET": "資產負債金額"
    }
    resp = requests.post(url, headers=headers, data=data)
    resp.encoding = "utf-8"
    
    if "您的瀏覽量異常, 已影響網站速度" in resp.text:
        raise Exception("您的瀏覽量異常, 已影響網站速度，我被抓包了")
    
    soup = BeautifulSoup(resp.text, "html.parser")
    
    rowList = []
    trList = soup.findAll("tr", id=re.compile("^row"))
    for tr in trList:
        row = []
        for td in tr.findAll("td"):
            text = td.text.strip().replace(",", "")
            row.append(text)
        rowList.append(row)
    
    with open("data_assetsStatus/{}.csv".format(stockId), "w", newline="", encoding="utf-8") as f1:
        writer = csv.writer(f1)
        writer.writerows(rowList)
        

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        lineTool.lineNotify(os.environ["LINE_TEST_TOKEN"], e)

'''
Created on 2018年6月6日
@author: Rocky
'''
import requests
from bs4 import BeautifulSoup
import re
import csv
import time

def main():
    
    stockId = "6024"
    qryTime = "20181"
     
    url = "https://goodinfo.tw/StockInfo/StockFinDetail.asp?STEP=DATA&STOCK_ID={}&RPT_CAT=IS_M_QUAR&QRY_TIME={}".format(stockId, qryTime)
    print("fetch url", url)
    headers = {
        "User-Agent" : "Chrome/31.0.1650.63",
        "referer": "https://goodinfo.tw/StockInfo/StockFinDetail.asp?RPT_CAT=IS_M_QUAR_ACC&STOCK_ID=6024"
    }
    r = requests.post(url, headers=headers)
    r.encoding = "utf-8"
    soup = BeautifulSoup(r.text, "html.parser")
    # get next qryTime (every 7 as a section)
    qryTimeOptions = soup.find("select", id="QRY_TIME").findAll("option")
    i = 1
    nextQryTimeList = []
    for option in qryTimeOptions:
        if (i-1) % 7 == 0:
            nextQryTimeList.append(option.text.replace("Q", ""))
        i += 1
          
    for qTime in nextQryTimeList:
        print("sleep and continue to ", qTime)
        time.sleep(5)
        fetch(stockId, qTime)

    
    
def fetch(stockId, qryTime):

    url = "https://goodinfo.tw/StockInfo/StockFinDetail.asp?STEP=DATA&STOCK_ID={}&RPT_CAT=IS_M_QUAR&QRY_TIME={}".format(stockId, qryTime)
    print("fetch url", url)
    
    headers = {
        "User-Agent" : "Chrome/31.0.1650.63",
        "referer" : "https://goodinfo.tw/StockInfo/StockFinDetail.asp?RPT_CAT=IS_M_QUAR_ACC&STOCK_ID=6024",
        "origin" : "https://goodinfo.tw" 
    }
    
    r = requests.post(url, headers=headers)
    r.encoding = "utf-8"
    
    soup = BeautifulSoup(r.text, "html.parser")
    
    # get all row data
    rowList = []
    trs = soup.findAll("tr", id=re.compile("^row"))
    for tr in trs:
        row = []
        for td in tr.findAll("td"):
            row.append(td.text)
        print(row)
        rowList.append(row)
            
    with open("finDetail_{}_{}.csv".format(stockId, qryTime), "w", encoding="utf-8", newline="") as f1:
        cw = csv.writer(f1)
        cw.writerows(rowList)

if __name__ == "__main__":
    main()
    
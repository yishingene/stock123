'''
董監外資持股每月明細

https://goodinfo.tw/StockInfo/StockDirectorSharehold.asp?STOCK_ID=6024

Created on 2018年6月6日
@author: Rocky
'''
import requests
from bs4 import BeautifulSoup
import re
import csv
import time
import os

folderPath = "stockDirectorSharehold"

def main():
    
    stockId = "1215"
    fetch(stockId)

    # 用來比對已經執行過的，不再重新執行
    existList = []
    for name in os.listdir():
        if name.startswith("StockDirectorSharehold"):
            stockId = name.split(".")[0].split("_")[1]
            print("append exist stockId ", stockId)
            existList.append(stockId)
    
    cnt = 0
    for name in os.listdir("../data"):
        if name == "t00.csv":
            continue
        
        stockId = name.split(".")[0]

        if stockId in existList:
            print("已有資料，不再重新抓取", name)
            continue
        
#         if stockId.startswith("0"):
#             print("先跳過", stockId)
#             continue
        
        cnt += 1 
        print(cnt)
        fetch(stockId)
 
        print("sleep x seconds then start...")
        time.sleep(5)



    
def fetch(stockId):

    url = "https://goodinfo.tw/StockInfo/StockDirectorSharehold.asp?STOCK_ID={}".format(stockId)
    print("fetch url", url)
    headers = {
        "User-Agent" : "Chrome/31.0.1650.63",
        "referer": "https://goodinfo.tw/StockInfo/StockDirectorSharehold.asp?STOCK_ID={}".format(stockId)
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
#         print(row)
        rowList.append(row)
            
    with open("StockDirectorSharehold_{}.csv".format(stockId), "w", encoding="utf-8", newline="") as f1:
        cw = csv.writer(f1)
        cw.writerows(rowList)
        
# def readFile(stockId):
#     
#     with open("StockDirectorSharehold_{}.csv".format(stockId), "r", encoding="utf-8", newline="") as f1:
#        rowList = list(csv.reader(f1))
#        
#     for row in rowList:
#         
#         if int(row[0].split("/")[0]) >= 2016:
#             print(row[0], row[12], row[13], row[14], row[15], row[16])
# #             print(row[0], row[7], row[8], row[9], row[10], row[11])
    

if __name__ == "__main__":
    main()
    
'''
月營收每月明細

Created on 2018年6月18日
@author: Rocky
'''
import requests
from bs4 import BeautifulSoup
import re
import csv
import time
import os
import lineTool
import traceback


def main():
    
#     stockId = "6024"
#     fetch(stockId)
#     readFile(stockId)

    # 用來比對已經執行過的，不再重新執行
    existList = []
    for name in os.listdir():
        if name.startswith("ShowSaleMonChart_"):
            stockId = name.split(".")[0].split("_")[1]
            existList.append(stockId)
     
    for name in os.listdir("../data"):
         
        stockId = name.split(".")[0]
        
        if stockId.startswith("0") or stockId == "t00":
            continue

#         with open("ShowSaleMonChart_{}.csv".format(stockId), "r") as f1:
#             row = list(csv.reader(f1))[0]
        
#         if row[0] == '2018/06':
#             continue

        if stockId in existList:
            continue
         
        fetch(stockId)
  
        print("sleep x seconds then start...")
        time.sleep(10)



    
def fetch(stockId):

    url = "https://goodinfo.tw/StockInfo/ShowSaleMonChart.asp?STOCK_ID={}".format(stockId)
    print("fetch url", url)
    headers = {
        "User-Agent" : "Chrome/31.0.1650.63",
        "referer": "https://goodinfo.tw/StockInfo/ShowSaleMonChart.asp?STOCK_ID={}".format(stockId)
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
            
    with open("ShowSaleMonChart_{}.csv".format(stockId), "w", encoding="utf-8", newline="") as f1:
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
    try:
        main()
    except:
        traceback.print_exc()
        lineTool.lineNotify(os.environ["LINE_TEST_TOKEN"], "fetchShowSaleMonChart error")
    
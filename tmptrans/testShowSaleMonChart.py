'''
月營收資料

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
    
#     fetch(stockId)
    
    readFile(stockId)
    
def fetch(stockId):

    url = "https://goodinfo.tw/StockInfo/ShowSaleMonChart.asp?STOCK_ID={}&STEP=DATA&CHT_CAT=ALL".format(stockId)
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
        print(row)
        rowList.append(row)
            
    with open("ShowSaleMonChart_{}.csv".format(stockId), "w", encoding="utf-8", newline="") as f1:
        cw = csv.writer(f1)
        cw.writerows(rowList)
        
def readFile(stockId):
    
    with open("ShowSaleMonChart_{}.csv".format(stockId), "r", encoding="utf-8", newline="") as f1:
       rowList = list(csv.reader(f1))
       
    for row in rowList:
        
        if int(row[0].split("/")[0]) >= 2016:
            print(row[0], row[12], row[13], row[14], row[15], row[16])
#             print(row[0], row[7], row[8], row[9], row[10], row[11])
    

if __name__ == "__main__":
    main()
    
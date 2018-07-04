'''
偵測是否有新資料出現

Created on 2018年7月3日
@author: rocky.wang
'''
import csv
from bs4 import BeautifulSoup
import requests
import re
import datetime
def main():
    
    print("# -------------------------- #\n# 執行時間 {} #\n# -------------------------- #".format(datetime.datetime.now().strftime('%Y/%m%d %H:%M:%S')))
    
    sid = "6024"
    detect(sid)
    
    # datetime.datetime.now().strftime('%Y/%m%d %H:%M:%S'))
    

def detect(sid):

    with open("StockDirectorSharehold_{}.csv".format(sid), "r") as f1:
        rowList = list(csv.reader(f1))[0:3]
        
    for row in rowList:
        print(row)

    print("read new data")
    with open("StockDirectorSharehold_{}_NEWTMP.csv".format(sid), "r") as f1:
        rowList = list(csv.reader(f1))[0:3]
        
    for row in rowList:
        print(row)


#     fetch(sid)


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
        rowList.append(row)

#     ym = datetime.datetime.now().strftime('%Y%m')
    
    with open("StockDirectorSharehold_{}_NEWTMP.csv".format(stockId), "w", encoding="utf-8", newline="") as f1:
        cw = csv.writer(f1)
        cw.writerows(rowList)

if __name__ == "__main__":
    main()
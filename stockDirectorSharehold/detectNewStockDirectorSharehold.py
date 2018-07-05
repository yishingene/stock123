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
import os
import time
from matplotlib.mlab import csv2rec
from future.backports.http.client import LineTooLong
import lineTool
import traceback
def main():
    
    print("# -------------------------- #\n# 執行時間 {} #\n# -------------------------- #".format(datetime.datetime.now().strftime('%Y/%m%d %H:%M:%S')))
    
#     sid = "1313"
#     fetch(sid)
#     detect(sid)
    cnt = 0
    for name in os.listdir("../data"):
        
        stockId = name.split(".")[0]
        
        if stockId == "t00" or stockId.startswith("0"):
            print("跳過 t00 與 0 開頭代號不需查詢", stockId)
            continue

        cnt += 1 
        print(cnt)
        
        try:
            fetch(stockId)
            detect(stockId)
        except:
            traceback.print_exc()
            print("error occur, try again")
            time.sleep(10)
            try:
                fetch(stockId)
                detect(stockId)
            except:
                traceback.print_exc()
                lineTool.lineNotify(os.environ["LINE_TEST_TOKEN"], "error occur when detect directorSharehold")
            
        print("sleep x seconds then start...")
        time.sleep(5)    
    
    
    
    # 前面 for 完全部，換通知
    
    if not os.path.exists("changeList.csv"):
        print("無任何異動不需通知")
        return

    print("\n開始進行通知\n")
    with open("changeList.csv", "r") as f1:
        rowList = list(csv.reader(f1))
    msg = "股權異動通知"
    for row in rowList:
        msg += "\n" + str(row)
        print(row)

    code = lineTool.lineNotify(os.environ["LINE_TEST_TOKEN"], msg)
    print(code)
    
    os.remove("changeList.csv")
    print("completed.")

def detect(sid):
    
    ym = datetime.datetime.now().strftime('%Y/%m')

    with open("StockDirectorSharehold_{}.csv".format(sid), "r") as f1:
        rowList = list(csv.reader(f1))[0:3]
    
    # 若舊檔沒有本月資料，直接把新檔變成舊檔就好
    if rowList[0][0] != ym:
        print("{} 無本月資料，僅將檔案更新".format(sid))
        os.remove("StockDirectorSharehold_{}.csv".format(sid)) # 移除舊檔
        os.rename("StockDirectorSharehold_{}_NEWTMP.csv".format(sid), "StockDirectorSharehold_{}.csv".format(sid))
        return
    
    with open("StockDirectorSharehold_{}_NEWTMP.csv".format(sid), "r") as f1:
        newRow = list(csv.reader(f1))[1]

    # 仍然沒有新的資料，移除新的暫存檔
    if newRow[-4] == '-':
        print("{} 仍無資料，移除暫存檔".format(sid))
        os.remove("StockDirectorSharehold_{}.csv".format(sid)) # 移除舊檔
        os.rename("StockDirectorSharehold_{}_NEWTMP.csv".format(sid), "StockDirectorSharehold_{}.csv".format(sid))
        return
    
    if newRow[-4] == '0':
        print("{} 本月有新資料但無異動，僅將檔案更新".format(sid))
        os.remove("StockDirectorSharehold_{}.csv".format(sid)) # 移除舊檔
        os.rename("StockDirectorSharehold_{}_NEWTMP.csv".format(sid), "StockDirectorSharehold_{}.csv".format(sid))
        return
    
    if newRow[-4] != '0' and newRow[-4] != rowList[1][-4]:
        newRow.insert(0, sid)
        print("{} 本月有新資料且股權異動 ! 寫入待通知檔 !".format(sid))
        print(newRow)
        os.remove("StockDirectorSharehold_{}.csv".format(sid)) # 移除舊檔
        os.rename("StockDirectorSharehold_{}_NEWTMP.csv".format(sid), "StockDirectorSharehold_{}.csv".format(sid))
        
        with open("changeList.csv", "a", newline="") as f1:
            writer = csv.writer(f1)
            writer.writerow(newRow)
    else:
        print("{} 本月有新資料且股權異動但已經通知過了".format(sid))
        os.remove("StockDirectorSharehold_{}.csv".format(sid)) # 移除舊檔
        os.rename("StockDirectorSharehold_{}_NEWTMP.csv".format(sid), "StockDirectorSharehold_{}.csv".format(sid))
    


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
'''
compare sids

Created on 2018年9月13日
@author: rocky.wang
'''
import csv
import requests
import datetime
import time

def main():
    
    with open("stockIds.csv", "r", encoding="utf-8") as f1:
        rowList = list(csv.reader(f1))

    print(len(rowList))
    
    newRowList = []
    
    for row in rowList:
#         if row[4] in ["上市", "上櫃"]:
#             newRowList.append(row)

        if row[4] in ["上市"]:
            newRowList.append(row)
    
    rowList = newRowList
    print(len(rowList))
    
    newRowList = []
    for row in rowList:
        if len(row[0]) == 4:
            newRowList.append(row)
        else:
            print("pass", row[0])
    
    rowList = newRowList
    print(len(rowList))
    
    print(rowList)
    
    
    
    sidList = fetchAllStockFinalData()
    
    for row in rowList:
        if not row[0] in sidList:
            print(row[0])
    
    




''' 收盤後，爬所有收盤股票資料 '''    
def fetchAllStockFinalData(dt=datetime.datetime.now()):
    
    url = "http://www.twse.com.tw/exchangeReport/MI_INDEX?response=json&date=%s&type=ALLBUT0999&_=%s" %(dt.strftime("%Y%m%d"), int(time.time()*1000))
    r = requests.get(url)
    print("GET %s\nResponse => %s" %(url, r.json()))
    
    js = r.json()
    if js.get("stat") != "OK":
        print("%s 查無資料" %(dt.strftime("%Y%m%d")))
        return
    
    sidList = []
    for data in js.get("data5"):
        
        sid = data[0]
        
        if len(sid) != 4:
            continue
        
        if data[9].find('red') > 0:
            sign = '+'
        else:
            sign = '-' if data[9].find('green') > 0 else ''
            
        date = "{}/{}/{}".format(js["date"][0:4], js["date"][4:6], js["date"][6:8])
#         row = [sid, date, data[2], data[4], data[5], data[6], data[7], data[8], sign+data[10], data[3], "", ""] # 後面兩個空值是 RSV & K9
#         rowList.append(row)
        sidList.append(sid)
        
    
    return sidList


if __name__ == "__main__":
    main()


'''
上市資料
Created on 2018年8月20日
@author: rocky.wang
'''
import datetime
import requests
import os
import time

''' 收盤後，爬所有收盤股票資料 '''    
def fetchAllStockFinalData(dt=datetime.datetime.now()):
    
    url = "http://www.twse.com.tw/exchangeReport/MI_INDEX?response=json&date=%s&type=ALLBUT0999&_=%s" %(dt.strftime("%Y%m%d"), int(time.time()*1000))
    r = requests.get(url)
    print("GET %s\nResponse => %s" %(url, r.json()))
    
    js = r.json()
    if js.get("stat") != "OK":
        print("%s 查無資料" %(dt.strftime("%Y%m%d")))
        return
    
    for data in js.get("data5"):
        print(data)
        
    print(len(js["data5"]))
        
        
if __name__ == "__main__":        
    fetchAllStockFinalData()
        

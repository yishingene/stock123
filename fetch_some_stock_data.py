'''
Created on 2018年3月29日
@author: rocky.wang
'''

from twse_crawler import TWSECrawler
import time

import sys
import datetime
from googleService import GooglesheetService
import lineTool
import os
import csv
import traceback
sys.path.append("/data/data/com.termux/files/home/stock123")

def main():
    print("\n執行時間 {}".format(datetime.datetime.now().strftime('%Y/%m%d %H:%M:%S')))

    t1 = time.time()
    crawler = TWSECrawler()
    
    # 爬大盤資料寫入 csv 檔
    crawler.fetchStockInfo("t00")
    time.sleep(2)
    crawler.fetchStockInfo("0050")
    time.sleep(2)
    crawler.fetchStockInfo("0056")
    time.sleep(2)
    
    rowList = [["代號", "名稱", "價格", "說明", "通知日期"]]
    
    # 我自己在 googlesheet 的觀注清單
    googlesheetService = GooglesheetService("1dFqFS_KLPIQDbuORvBKrMQEXgv8AYN6VNYvaZvYpVTk")
    for value in googlesheetService.getValues("低價買入!A2:Z10000"):
        
        crawler.fetchStockInfo(value[0])

        with open("data/{}.csv".format(value[0]), encoding="MS950") as f1:
            if len(value) == 4:
                value.append("") # 補齊「通知日期」欄位，避免 index out of range
            # 取最後一行
            row = list(csv.reader(f1))[-1]
            # 金額已跌破，並且沒有通知過 (日期不相同)
            if float(row[6]) <= float(value[2]) and value[4] != row[0]:
                lineTool.lineNotify(os.environ["LINE_TEST_TOKEN"], "{} {}，欲買進價格 {}，目前 {}，{}".format(value[0], value[1], value[2], row[6], value[3]))
                value[4] = row[0]
        
        rowList.append(value)
        time.sleep(2)
    
    t2 = int(time.time() - t1)
    
    googlesheetService.updateSheet("低價買入", rowList)
    
    print("fetch some total time {} seconds".format(t2))
    

    
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        lineTool.lineNotify(os.environ["LINE_TEST_TOKEN"], "fetch_some_stock_data 發生錯誤")

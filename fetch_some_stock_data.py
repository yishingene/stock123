'''
Created on 2018年3月29日
@author: rocky.wang
'''

from twse_crawler import TWSECrawler
import time

import sys
import datetime
from googleService import GooglesheetService
sys.path.append("/data/data/com.termux/files/home/stock123")

def main():
    print("執行時間 {}".format(datetime.datetime.now().strftime('%Y/%m%d %H:%M:%S')))

    t1 = time.time()
    crawler = TWSECrawler()
    
    # 爬大盤資料寫入 csv 檔
    crawler.fetchStockInfo("t00")
    time.sleep(1)
    crawler.fetchStockInfo("0050")
    time.sleep(1)
    crawler.fetchStockInfo("0056")
    time.sleep(1)
    
    # 我自己在 googlesheet 的觀注清單
    googlesheetService = GooglesheetService("1dFqFS_KLPIQDbuORvBKrMQEXgv8AYN6VNYvaZvYpVTk")
    cnt = -1
    for value in googlesheetService.getValues("低價買入"):
        cnt += 1
        if cnt == 0:
            continue
        crawler.fetchStockInfo(value[0])
        time.sleep(1)
    
    t2 = int(time.time() - t1)
    
    print("fetch some total time {} seconds".format(t2))
    

    
if __name__ == "__main__":
    main()


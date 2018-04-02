'''
抓取盤後資料寫回 csv 檔，注意要排程式下午 1:50 分鐘後才會有資料

Created on 2018年3月27日
@author: rocky.wang
'''
from twse_crawler import TWSECrawler
import datetime
import time

import sys
sys.path.append("/data/data/com.termux/files/home/stock123")

def main():

    t1 = time.time()
    now = datetime.datetime.now()
    
    crawler = TWSECrawler()
    
    # 13:50 分以後才會有資料
    if int(str(now.hour) + format(now.minute, "02")) >= 1350:
        # 爬資料寫到各 csv 檔
        crawler.fetchAllStockFinalData()
        
      
    # 爬大盤資料寫入 csv 檔
    crawler.fetchStockInfo("t00")
    
    t2 = int(time.time() - t1)
    print("total time {}".format(t2))
    
    
if __name__ == "__main__":
    main()


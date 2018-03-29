'''
抓取盤後資料寫回 csv 檔，注意要排程式下午 1:50 分鐘後才會有資料

Created on 2018年3月27日
@author: rocky.wang
'''
from twse_crawler import TWSECrawler
import datetime
import time

def main():

    now = datetime.datetime.now()
    
    crawler = TWSECrawler()
    
    dt = datetime.datetime(2018, 3, 28)
    
    if int(str(now.hour) + format(now.minute, "02")) >= 1207:
        # 爬資料寫到各 csv 檔
        crawler.fetchAllStockFinalData(dt)
#         crawler.fetchAllStockFinalData()
      
    print("sleeping 5 seconds...")
    time.sleep(5)
      
    # 爬大盤資料寫入 csv 檔
    crawler.fetchStockInfo("t00")
    
    
    
if __name__ == "__main__":
    main()


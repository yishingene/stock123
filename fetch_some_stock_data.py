'''
Created on 2018年3月29日
@author: rocky.wang
'''

from twse_crawler import TWSECrawler
import time

import sys
sys.path.append("/data/data/com.termux/files/home/stock123")

def main():

    crawler = TWSECrawler()
    
    # 爬大盤資料寫入 csv 檔
    crawler.fetchStockInfo("t00")
    time.sleep(2)
    crawler.fetchStockInfo("0050")
    time.sleep(2)
    crawler.fetchStockInfo("0056")
    
    
if __name__ == "__main__":
    main()


'''
Created on 2018年4月16日
@author: rocky.wang
'''

from twse_crawler import TWSECrawler
import time

import sys
import datetime
import traceback
sys.path.append("/data/data/com.termux/files/home/stock123")

def main():
    crawler = TWSECrawler()
    
    # 4205 
    # 6803  應該都是上櫃，所以查不到，而且我也沒詳細資料
    
    # 爬大盤資料寫入 csv 檔
    crawler.fetchStockInfo("9926")
    
    
    

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        traceback.print_exc()
#         lineTool.lineNotify(os.environ["LINE_TEST_TOKEN"], "fetch_some_stock_data 發生錯誤")

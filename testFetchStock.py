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
    print("\n執行時間 {}".format(datetime.datetime.now().strftime('%Y/%m%d %H:%M:%S')))

    t1 = time.time()
    crawler = TWSECrawler()
    
    # 爬大盤資料寫入 csv 檔
    crawler.fetchStockInfo("9918")
    
    t2 = int(time.time() - t1)
    
    print("test fetch total time {} seconds".format(t2))
    

    
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        traceback.print_exc()
#         lineTool.lineNotify(os.environ["LINE_TEST_TOKEN"], "fetch_some_stock_data 發生錯誤")

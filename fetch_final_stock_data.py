'''
抓取盤後資料寫回 csv 檔
Created on 2018年3月27日
@author: rocky.wang
'''
from twse_crawler import TWSECrawler
import appendRSAK9
import time

def main():
    
    beginTime = time.time()
    
    crawler = TWSECrawler()
    crawler.fetchAllStockFinalData()
    
    appendRSAK9.main()
    
    endTime = time.time()
    print(endTime - beginTime)

def processData(js):
    
    pass



if __name__ == "__main__":
    main()


'''
抓取盤後資料寫回 csv 檔，注意要排程式下午 1:50 分鐘後才會有資料

Created on 2018年3月27日
@author: rocky.wang
'''
from twse_crawler import TWSECrawler
import appendRSAK9

def main():
    # 爬資料寫到各 csv 檔
    crawler = TWSECrawler()
    crawler.fetchAllStockFinalData()
    
if __name__ == "__main__":
    main()


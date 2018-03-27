'''
Created on 2018年3月27日
@author: rocky.wang
'''
from twse_crawler import TWSECrawler
import csv

def main():
    
    filename = "t00.csv"
    
    rowDict = {}
    # 抓舊資料
    with open(filename) as f1:
        for row in csv.reader(f1):
            
            if row[0] == "日期":
                rowDict[row[0]] = row
                continue
            
            if not row[0].startswith("20") and not row[0].startswith("19"):
                row[0] = row[0].strip()
                row[0] = str(int(row[0].split("/")[0]) + 1911) + "/{}/{}".format(row[0].split("/")[1], row[0].split("/")[2])
                
            rowDict[row[0]] = row
    
    # 爬今日的
    twseCrawler = TWSECrawler()
    
    js = twseCrawler.fetchStockInfo("t00")
    
    # 20180327 => 2018/03/27
    dt = "{}/{}/{}".format(js["msgArray"][0]["d"][0:4], js["msgArray"][0]["d"][4:6], js["msgArray"][0]["d"][6:8])
    
    row = [dt, js["msgArray"][0]["o"], js["msgArray"][0]["h"], js["msgArray"][0]["l"], js["msgArray"][0]["z"]]
    rowDict[row[0]] = row
    
    with open(filename, "w", newline="") as f1:
        writer = csv.writer(f1)
        for d in rowDict.values():
            writer.writerow(d)



if __name__ == "__main__":
    main()






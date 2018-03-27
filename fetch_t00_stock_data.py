'''
Created on 2018年3月27日
@author: rocky.wang
'''
from twse_crawler import TWSECrawler
import csv
from matplotlib.mlab import csv2rec

twseCrawler = TWSECrawler()

js = twseCrawler.fetchStockInfo("t00")

header = ["日期", "開盤價", "最高價", "最低價", "收盤價", "RSV", "K9"]

rowDict = {}
rowDict[header[0]] = header

with open("t00.csv") as f1:
    for row in csv.reader(f1):
        row[0] = row[0].strip()
        row[0] = str(int(row[0].split("/")[0]) + 1911) + "/{}/{}".format(row[0].split("/")[1], row[0].split("/")[2])
        
        row[1] = float(row[1])
        row[2] = float(row[2])
        row[3] = float(row[3])
        row[4] = float(row[4])
        row[5] = float(row[5])
        row[6] = float(row[6])
        
        rowDict[row[0]] = row
        

with open("t00new.csv", "w", newline="") as f1:
    writer = csv.writer(f1)
    for d in rowDict.values():
        writer.writerow(d)





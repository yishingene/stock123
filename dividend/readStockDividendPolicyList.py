'''

Created on 2018年6月9日
@author: Rocky
'''
import csv
import os
import requests
import datetime
import time

def main():    
    
    for filename in os.listdir("data"):
        stockId = filename.split("_")[0]
        processStockId(stockId)


def processStockId(stockId):
    
    # 取配息資料
    stockName, subList, avgM = readDividend(stockId)
    newM = subList[0]
    
    try:
        # 取最新股價
        with open("../data/{}.csv".format(stockId), "r") as f1:
            rowList = list(csv.reader(f1))
            price = float(rowList[-1][6])
    except FileNotFoundError:
#         print("not found for ", stockId)
        price = 1000
        
    newRate = round(newM / price * 100, 2)
    avgRate = round(avgM / price * 100, 2)
    
    if avgRate >= 6.25 and newRate >= 5:
        if stockId == "2939":
            subList.append(0)
            subList.append(0)
            subList.append(0)
        if stockId in ["6582", "8466", "8481"]:
            subList.append(0)
            subList.append(0)
        print("{},{},{},{},{},{},{},{},{},{}".format(stockId, stockName, price, avgRate, newRate, subList[0], subList[1], subList[2], subList[3], subList[4]))

#     print(stockId, stockName, price, newM, avgM, newRate, avgRate)
    
def readDividend(stockId):
    
    with open("data/{}_stockDividendPolicyList.csv".format(stockId), "r", encoding="utf-8") as f1:
        
        mList = []
        for row in csv.reader(f1):
            stockId = row[1]
            stockName = row[2]
            year = row[3]
            pureEarn = row[4] # 稅後淨利 (億)
            eps = row[5]
            m = row[8]
            s = row[11]
            # 現金殖利率
            mList.append(float(m))
            
#             print(stockId, stockName, year, pureEarn, eps, m, s)
            
        mList.reverse()
        subList = mList[:5]

#         print(sum(subList[-5:]))
        return stockName, subList, round(sum(subList) / len(subList), 2)
        
        
        
if __name__ == "__main__":
    main()
'''
Created on 2018年6月18日
@author: Rocky
'''
import os
import csv
from operator import itemgetter


def main():
    
    stockIdNameMap = {}
    with open("../stockIds.csv", "r", encoding="utf-8") as f1:
        rowList = list(csv.reader(f1))
        for row in rowList:
            stockIdNameMap[row[0]] = row[1]
    
    dataList = []
    for name in os.listdir():
        
        if not name.startswith("StockDirectorSharehold"):
            continue
        
        with open(name, "r") as f1:
            rowList = list(csv.reader(f1))
        
        # 先取最新月份 (第一行)，若沒資料再取次月，最多取到次次月
        row = rowList[0]
        if row[17] == '-':
            row = rowList[1]
        if row[17] == '-':
            row = rowList[2]
        if row[17] == '-':
            continue
        amt = int(row[17].replace(",", ""))
        
        if amt > 0 or amt < 0: 
            dataList.append(row)
            stockId = name.split(".")[0].split("_")[1]
            stockName = stockIdNameMap.get(stockId)
            row.append(stockId)
            row.append(stockName)
            row.append(int(amt)) # 為了排序
        
    dataList = sorted(dataList, key=itemgetter(23), reverse=True)

    for row in dataList:
        price = 'N/A  '
        if row[1] != '-':
            price = round(float(row[1]), 2) # 為了對齊，float 會補 0，round 應該沒用
        print("{} {}\t{}\t{}\t{}".format(row[21], row[22], row[0], price, row[17]))
            

if __name__ == "__main__":

    main()

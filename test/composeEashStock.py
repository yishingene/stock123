'''
把各年份的組成個股的各個殖利率檔

Created on 2018年3月31日
@author: rocky.wang
'''
import os
import csv

allDataDict = {}

for name in os.listdir():
    
    if name.endswith("dividend.csv"):
        
        print(name)
        
        with open(name, "r", encoding="utf-8") as f1:
            for row in csv.reader(f1):
                stockId = row[1]
                stockData = allDataDict.get(stockId, None)
                
                if stockData == None:
                    stockData = []
                    allDataDict[stockId] = stockData
                
                stockData.append(row)    
        
for stockData in allDataDict.values():

    stockId = stockData[0][1]

    with open("data2/{}.csv".format(stockId), "w", newline="", encoding="utf-8") as f1:
        wr = csv.writer(f1)
        for row in stockData:
            wr.writerow(row)

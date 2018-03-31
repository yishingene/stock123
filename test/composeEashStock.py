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
        
for v in allDataDict.values():

    stockId = v[0][1]

    
    
    for d in v:
        print(d)
    print("----------------------")    

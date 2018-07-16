'''
把各年份的組成個股的各個殖利率檔

Created on 2018年3月31日
@author: rocky.wang
'''
import os
import csv

allDataDict = {}

# 讀取資料
for name in os.listdir():
    
    if name.endswith("stockDividendPolicyList.csv"):
        with open(name, "r", encoding="utf-8") as f1:
            for row in csv.reader(f1):
                # 過濾掉不是上市/上櫃的資料
                # TODO 我沒有上櫃的資料，只能先處理上市
#                 if row[0] != '上市' and row[0] != '上櫃':
                if row[0] != '上市':
                    continue
                
                stockId = row[1]
                stockData = allDataDict.get(stockId, None)
                if stockData == None:
                    stockData = []
                    allDataDict[stockId] = stockData
                 
                stockData.append(row)    
         
for stockData in allDataDict.values():
 
    if not os.path.exists("data"): 
        os.makedirs("data")
 
    stockId = stockData[0][1]
 
    with open("data/{}_stockDividendPolicyList.csv".format(stockId), "w", newline="", encoding="utf-8") as f1:
        wr = csv.writer(f1)
        for row in stockData:
            wr.writerow(row)

print("completed")
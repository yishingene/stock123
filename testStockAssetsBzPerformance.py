'''
抓取稅後淨利 & 長期負債做計算

testStockAssetsStatus.py & testStockBzPerformance.py 的統整

Created on 2018年4月8日
@author: rocky.wang
'''
from testStockAssetsStatus import fetchStockAssetsStatus
from testStockBzPerformance import fetchStockBzPerformance
 
stockId = "2382"
 
longTermDebit = fetchStockAssetsStatus(stockId)
pureEarn = fetchStockBzPerformance(stockId)
  
rate = round(longTermDebit / pureEarn, 2)
  
print("長期負債: {}, 盈收: {}, 比例: {}".format(longTermDebit, pureEarn, rate))


# import os
# import csv
# 
# for filename in os.listdir("data_assetsStatus"):
#     stockId = filename.split(".")[0]
#     
#     # file is empty
#     if os.stat("data_assetsStatus/{}".format(filename)).st_size == 0:
#         continue
#     
#     if filename != "1264.csv":
#         continue
#     
#     with open("data_assetsStatus/{}".format(filename), encoding="utf-8") as f1:
#         print(filename)
#         row = list(csv.reader(f1))[0]
#         print(row[18])
        

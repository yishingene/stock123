'''
Created on 2018年5月14日
@author: rocky.wang
'''
import csv

with open("stockIds.csv", encoding="utf-8") as f1:
    rowList = list(csv.reader(f1))
stockMap = {}    
for row in rowList:
    stockMap[row[0]] = row[4]
    
# print(stockMap)

stockId = "4205"

print(stockMap.get(stockId))


s = 'IFERROR(ARRAY_CONSTRAIN(importXML(CONCATENATE("http://m.wantgoo.com/s/", $A{}),"//*/div[2]/div/div[1]"),1,1))'.format(20)

print(s)
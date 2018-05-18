'''
無聊計算每年的殖利率變化

Created on 2018年5月9日
@author: rocky.wang
'''
import csv

with open("1232_dividendSchedule.csv") as f1:
    
    rowList = list(csv.reader(f1))[:5]

for row in rowList:
    print(row)
    avgPrice = row[-2]
    avgRate = row[-1]
    print(avgPrice, avgRate)
    


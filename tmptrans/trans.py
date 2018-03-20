'''
Created on 2018年3月20日
@author: rocky.wang
'''
from googleService import GooglesheetService
import os, json, requests, csv

header = ["日期","開盤指數","最高指數","最低指數","收盤指數", "RSV", "K9"]

rowList = [header]

with open("0000withRSVK9.csv") as f1:
    for row in csv.reader(f1):
        rowList.append(row)

# 初使前面幾筆沒有 K 值為 50
for row in rowList:
    
    if row[0] == "日期":
        continue
    
    row[0] = row[0].strip()
    row[0] = "{}/{}/{}".format(int(row[0].split("/")[0]) + 1911, row[0].split("/")[1], row[0].split("/")[2])
    
    if row[6] == '':
        row[6] = 50
        


rowListMap = {}    
for row in rowList:
    rowListMap[row[0]] = row

print(rowListMap)


sheetService = GooglesheetService("1033HVmaLyxYkfiX889L5J4ypBuw9xvowotKGPtXWRV0")
rangeName = "T00"
sheetService.clearSheet(rangeName)
sheetService.updateSheet(rangeName, rowList)










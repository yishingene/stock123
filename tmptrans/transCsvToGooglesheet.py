'''
csv to googlesheet

Created on 2018年3月22日
@author: rocky.wang
'''
import os
from googleService import GooglesheetService
import csv

# operate https://docs.google.com/spreadsheets/d/1033HVmaLyxYkfiX889L5J4ypBuw9xvowotKGPtXWRV0/edit#gid=0
googlesheetService = GooglesheetService("1033HVmaLyxYkfiX889L5J4ypBuw9xvowotKGPtXWRV0")

# get all sheets range name
rangeNameList = googlesheetService.getRangeNameList()

def main():
    
    for filename in os.listdir("data"):
        stockId = filename.strip(".csv")
        processCsvToGooglesheet(stockId)
    
#     processCsvToGooglesheet("0050")
        
    pass



def processCsvToGooglesheet(stockId):
    
    print("process stockId {}...".format(stockId))
    
    # create sheet for stockId if not exist
#     if not stockId in rangeNameList:
#         googlesheetService.addSheet(stockId)
    
    googlesheetService.deleteSheetByRangeName(stockId)

    googlesheetService.addSheet(stockId)
    
    rowList = []
    header = ["日期","成交股數","成交金額","開盤價","最高價","最低價","收盤價","漲跌價差","成交筆數", "RSV", "K9"]
    rowList.append(header)
    
    with open("data/{}.csv".format(stockId)) as f1:
        for row in csv.reader(f1):
            yyyy = int(row[0].split("/")[0]) + 1911
            row[0] = "{}/{}/{}".format(yyyy, row[0].split("/")[1], row[0].split("/")[2])
            rowList.append(row)
    
    googlesheetService.updateSheet(stockId, rowList)
    
    
        


if __name__ == "__main__":
    main()





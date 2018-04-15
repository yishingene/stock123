'''
Created on 2018年4月15日
@author: Rocky
'''
import csv
import os
from googleService import GooglesheetService

def main():
    
    rowList = []
    for filename in os.listdir("data"):
        sid = filename.split(".")[0]
        row = process(sid)
        if row != None:
            rowList.append(row)

#     sid = "00636K"
#     process(sid)
    
    # TODO 過濾只有 SHEET 裡有的再印
    googlehseetService = GooglesheetService("")
    
    rowList = sorted(rowList, key=lambda row: row[3], reverse=True)
    print("---------------------")
    for row in rowList:
        print("{}\t{}  {}\t{}".format(row[0], row[1], row[2], row[3]))
    
    pass

def process(stockId):
    rtnRow = None
    with open("data/{}.csv".format(stockId)) as f1:
        reader = csv.reader(f1)
        next(reader) # 略過 header
        rowList = list(reader)[-250:]
        
        lastRow = rowList[-1]
        lastPrice = float(lastRow[6])
        
        rowList = sorted(rowList, key=lambda row: row[6], reverse=False) # reverse=False，最後一筆是最高值
        
        highPrice = float(rowList[-1][6])
        
        if highPrice - lastPrice > 0:
            
            diffPct = round(lastPrice / highPrice, 2)
            if diffPct < 0.99:
                rtnRow = [stockId, highPrice, lastPrice, diffPct]
#                 print("{}\t{}  {}\t{}".format(stockId, highPrice, lastPrice, diffPct))
        
    return rtnRow

if __name__ == "__main__":
    main()


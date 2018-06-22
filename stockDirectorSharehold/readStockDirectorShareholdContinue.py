'''
Created on 2018年6月18日
@author: Rocky
'''
import os
import csv


def main():
    
    stockIdNameMap = {}
    with open("../stockIds.csv", "r", encoding="utf-8") as f1:
        rowList = list(csv.reader(f1))
        for row in rowList:
            stockIdNameMap[row[0]] = row[1]
    
    
    for name in os.listdir():
        
        if not name.startswith("StockDirectorSharehold"):
            continue
        
        with open(name, "r") as f1:
            rowList = list(csv.reader(f1))
        
        # 連讀三行，避開 0050 之類沒資料的
        row = rowList[0]
        if row[17] == '-':
            row = rowList[1]
        if row[17] == '-':
            row = rowList[2]
        if row[17] == '-':
            continue
        
        try:
            amt1 = int(rowList[1][17].replace(",", ""))
            amt2 = int(rowList[2][17].replace(",", ""))
            amt3 = int(rowList[3][17].replace(",", ""))
        except:
            print(name)
            print(row)
            
        if amt1 > 0 and amt2 > 0: 
            
            stockId = name.split(".")[0].split("_")[1]
            stockName = stockIdNameMap.get(stockId)
            price = 'N/A  '
            pct = int(row[17].replace(",", "")) / int(row[15].replace(",", "")) * 100
            pct = round(pct, 2)
            if row[1] != '-':
                price = round(float(row[1]), 2) # 為了對齊，float 會補 0，round 應該沒用
            print("{} {}\t{}\t收盤 {}\t持股張數 {} ({}%)\t外資持股 {}%\t{}\t{}".format(stockId, stockName, row[0], price, row[15], row[16], row[19], row[17], pct))
        
    
#     with open("StockDirectorSharehold_1313.csv", "r") as f1:
#         rowList = list(csv.reader(f1))
#          
#     for row in rowList:
#         price = 'N/A  '
#         if row[1] != '-':
#             price = round(float(row[1]), 2) # 為了對齊，float 會補 0，round 應該沒用
#         print("{}\t{}\t{}".format(row[0], price, row[17]))
    
# for row in rowList:
#     print(row[0], row[17])

if __name__ == "__main__":

    main()

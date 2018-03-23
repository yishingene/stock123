'''
upload dividend data to 
https://docs.google.com/spreadsheets/d/1Zgl32clbWwwOTOP9mW9eOHiE8uojXmRgVjxvxQvjscM/edit?usp=sharing

Created on 2018年3月20日
@author: Rocky
'''
import os
from tmptrans.googleService import GooglesheetService
import csv

filenames = os.listdir()

filenames = [filename for filename in filenames if filename.endswith(".csv")]

print(filenames)

googlesheetService = GooglesheetService("1Zgl32clbWwwOTOP9mW9eOHiE8uojXmRgVjxvxQvjscM")

filenames.reverse()

for filename in filenames:
    
    rowList = [["市場", "代碼", "股票名稱", "股利所屬年度", "股東會日期", "除息交易日", "除息參考價(元)", "除權交易日", "除權參考價(元)", "現金股利發放日", "現金股利盈餘", "現金股利公積", "現金股利合計", "股票股利盈餘", "股票股利公積", "股票股利合計", "股利合計"]]
    
    with open(filename, encoding="utf-8") as f1:
        print(filename)
        for row in csv.reader(f1):
            rowList.append(row)
            
    rangeName = filename.replace(".csv", "")

    googlesheetService.addSheet(rangeName)
    googlesheetService.clearSheet(rangeName)
    googlesheetService.updateSheet(rangeName, rowList)

#     try:
#         googlesheetService.addSheet(rangeName)
#         googlesheetService.clearSheet(rangeName)
#         googlesheetService.updateSheet(rangeName, rowList)
#     except:
#         pass

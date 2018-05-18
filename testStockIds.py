'''
寫入公式到 googlesheet 產生所有的基本價格資料

Created on 2018年5月18日
@author: rocky.wang
'''
import csv
from googleService import GooglesheetService

googlesheetService = GooglesheetService("1v_h_IGT9gRYqm1jIf4N413k1KqwGRKwxYx0_ww5Tnz0")

def main():
    
    readFromGooglesheet()
#     writeToGooglesheet()
    
    print("completed")

def readFromGooglesheet():
    
    rowList = googlesheetService.getValues("工作表4")
    
    rowNum = 0
    for row in rowList:
        rowNum += 1
        if rowNum == 1:
            continue
        if row[4] == '#N/A':
            continue
        # 跌幅大於 2% 的
        if float(row[4]) <= -2:
            print(row)
    
    

def writeToGooglesheet():
    
    with open("stockIds.csv", encoding="utf-8") as f1:
        rowList = list(csv.reader(f1))

    sheetRowList = [["代號", "名稱", "價格", "漲跌", "漲跌幅", "成交量", "開盤價", "最高價", "最低價", "本益比"]]    
    cnt1 = 0
    cnt2 = 0
    rowNum = 1
    for row in rowList:
        if row[4] == '上市':
            # 過濾 03, 04, 05, 06，07 開頭，並且長度是六碼的，是什麼購的，googlefinance 也抓不出價格
            isStartWith0x = row[0].startswith("03") or row[0].startswith("04") or row[0].startswith("05") or row[0].startswith("06") or row[0].startswith("07") 
            if isStartWith0x and len(row[0]) == 6:
                continue
            
            cnt1 += 1
            rowNum += 1
            
            sheetRow = [row[0], row[1], 
                        '=GOOGLEFINANCE(CONCATENATE("TPE:", $A{}), "price")'.format(rowNum),
                        '=GOOGLEFINANCE(CONCATENATE("TPE:", $A{}), "change")'.format(rowNum),
                        '=GOOGLEFINANCE(CONCATENATE("TPE:", $A{}), "changepct")'.format(rowNum),
                        '=GOOGLEFINANCE(CONCATENATE("TPE:", $A{}), "volume")'.format(rowNum),
                        '=GOOGLEFINANCE(CONCATENATE("TPE:", $A{}), "priceopen")'.format(rowNum),
                        '=GOOGLEFINANCE(CONCATENATE("TPE:", $A{}), "high")'.format(rowNum),
                        '=GOOGLEFINANCE(CONCATENATE("TPE:", $A{}), "low")'.format(rowNum),
                        '=GOOGLEFINANCE(CONCATENATE("TPE:", $A{}), "pe")'.format(rowNum),
                        ]
            sheetRowList.append(sheetRow)
            
        if row[4] == '上櫃':
            cnt2 += 1
            
    googlesheetService.clearSheet("工作表4")
    googlesheetService.updateSheet("工作表4", sheetRowList)


if __name__ == "__main__":
    main()

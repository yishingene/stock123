'''

Created on 2018年5月14日
@author: rocky.wang
'''
import sys
import datetime
from googleService import GooglesheetService
import lineTool
import os
import traceback
import csv
import time
sys.path.append("/data/data/com.termux/files/home/stock123")

# 建立 map 用來判斷該股是上市或上櫃
with open("stockIds.csv", encoding="utf-8") as f1:
    rowList = list(csv.reader(f1))
stockIdMap = {}    
for row in rowList:
    stockIdMap[row[0]] = row[4] # stockId : 上市/上櫃


def main():
    print("執行時間 {}".format(datetime.datetime.now().strftime('%Y/%m%d %H:%M:%S')))

    sheetDataList = fetchAllSheetDataListFromMyGooglehseet()
    
    for sheetData in sheetDataList:
        print("處理 {} 資料 {}/{}, Token: {}".format(sheetData[0], sheetData[1], sheetData[3], sheetData[2]), flush=True)
        processSheet(sheetData[1], sheetData[3], sheetData[2])
        time.sleep(0.5)
 
    print('執行完畢')



def fetchAllSheetDataListFromMyGooglehseet():
    
    googlesheetService = GooglesheetService("1F3cT6ltHQ7gOYxCPSrPJGvMpUt3b5mRJIMR0gJ5ITr8")
    rowList = googlesheetService.getValues("掃描清單")
    rowNum = 0
    sheetDataList = []
    for row in rowList:
        rowNum += 1
        if rowNum == 1:
            continue
        if len(row) == 0 or row[0] == '' and row[1] == '':
            continue # 略過空白行
        
        sheetId = row[1].replace("https://docs.google.com/spreadsheets/d/", "").split("/")[0]
        # name, sheetId, token, rangeName
        sheetDataList.append([row[0], sheetId, row[2], row[3]])
        
    return sheetDataList


def processSheet(sheetId, sheetName, notifyLineToken):

    googlesheetService = GooglesheetService(sheetId)
    
    rowNum = 0    
    rowList = []
    msg = ""
    for value in googlesheetService.getValues(sheetName):
        rowNum += 1
        rowList.append(value)
        
        # header
        if rowNum == 1:
            if len(value) <= 10:
                value.append("") 
            columnNum = len(value) # 取 header 的總 column 數
            value[10] = datetime.datetime.now().strftime('%m%d %H:%M:%S')
            continue # header 不繼續下面的邏輯
        
        if len(value) == 0:
            continue # 略過空白行
        # 明細列若欄位不足，先補齊，避免 exception 發生
        if len(value) < columnNum:
            for i in range(columnNum - len(value)):
                value.append("")

        if value[0] == '':
            continue # 連代號都沒有，其他卻還有 #N/A 的值，大家還是會亂搞，防呆

        # 開始比價
        try:
            nowPrice = float(value[4].replace(",", ""))
        except:
            print("something wrong", value[4])
            nowPrice = 5000.0

        wantPrice = value[2]
        
#         if nowPrice != "" and wantPrice != "" and nowPrice <= float(wantPrice):
        if wantPrice != "" and nowPrice <= float(wantPrice):
            if value[10] != datetime.datetime.now().strftime('%Y%m%d'):
                msg += "\n{} ({}) 買進價 {}，現價 {}，PE: {}，買進原因： {}\n".format(value[1], value[0], value[2], value[4], value[8], value[9])
                value[10] = datetime.datetime.now().strftime('%Y%m%d')
        
        if stockIdMap[value[0]] == "上櫃":
#             value[3] = '=(E{}-C{})/C{}'.format(rowNum, rowNum, rowNum)
#             value[4] = '=IFERROR(ARRAY_CONSTRAIN(importXML(CONCATENATE("http://m.wantgoo.com/s/", $A{}),"//*/div[2]/div/div[1]"),1,1))'.format(rowNum)
#             value[5] = 'N/A'
#             value[6] = 'N/A'
#             value[7] = 'N/A'
#             value[8] = 'N/A'
#             print("上櫃資料改由別隻處理")
            pass
        else:
            value[3] = '=(E{}-C{})/C{}'.format(rowNum, rowNum, rowNum)
            value[4] = '=GOOGLEFINANCE(CONCATENATE("TPE:", $A{}), "price")'.format(rowNum)
            value[5] = '=GOOGLEFINANCE(CONCATENATE("TPE:", $A{}), "change")'.format(rowNum)
            value[6] = '=GOOGLEFINANCE(CONCATENATE("TPE:", $A{}), "changepct") / 100'.format(rowNum)
            value[7] = '=GOOGLEFINANCE(CONCATENATE("TPE:", $A{}), "volume") / 1000'.format(rowNum)
            value[8] = '=GOOGLEFINANCE(CONCATENATE("TPE:", $A{}), "pe")'.format(rowNum)

    # 其實應該只要更新時間欄位就好，其他欄位不要再更新，但我懶的再改了，之後再說
    googlesheetService.updateSheet(sheetName, rowList)

    if msg != '':
        print("notify msg => {}".format(msg), flush=True)
        lineTool.lineNotify(notifyLineToken, msg)
        
    
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        lineTool.lineNotify(os.environ["LINE_TEST_TOKEN"], "notifyRockyPrice 發生錯誤")

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
sys.path.append("/data/data/com.termux/files/home/stock123")

def main():
    print("執行時間 {}".format(datetime.datetime.now().strftime('%Y/%m%d %H:%M:%S')))

    # 建立 map 用來判斷該股是上市或上櫃
    with open("stockIds.csv", encoding="utf-8") as f1:
        rowList = list(csv.reader(f1))
    stockIdMap = {}    
    for row in rowList:
        stockIdMap[row[0]] = row[4] # stockId : 上市/上櫃

    # 我自己在 googlesheet 的觀注清單 v2
    googlesheetService = GooglesheetService("1F3cT6ltHQ7gOYxCPSrPJGvMpUt3b5mRJIMR0gJ5ITr8")
    
    rowNum = 0    
    rowList = []
    msg = ""
    for value in googlesheetService.getValues("工作表1!A1:Z10000"):
        rowNum += 1
        rowList.append(value)
        
        # header
        if rowNum == 1:
            columnNum = len(value) # 取 header 的總 column 數
            value[9] = datetime.datetime.now().strftime('%m%d %H:%M:%S')
            continue # header 不繼續下面的邏輯
        
        if len(value) == 0:
            continue # 略過空白行
        # 明細列若欄位不足，先補齊，避免 exception 發生
        if len(value) < columnNum:
            for i in range(columnNum - len(value)):
                value.append("")

        # 開始比價
        nowPrice = value[4]
        wantPrice = value[2]
        if nowPrice < wantPrice:
            if value[9] != datetime.datetime.now().strftime('%Y%m%d'):
                msg += "\n{} ({}) 買進價 {}，現價 {}，PE: {}，買進原因： {}\n".format(value[1], value[0], value[2], value[4], value[7], value[8])
                value[9] = datetime.datetime.now().strftime('%Y%m%d')
        
        value[3] = '=(E{}-C{})/C{}'.format(rowNum, rowNum, rowNum)
        if stockIdMap[value[0]] == "上櫃":
            value[4] = '=IFERROR(ARRAY_CONSTRAIN(importXML(CONCATENATE("http://m.wantgoo.com/s/", $A{}),"//*/div[2]/div/div[1]"),1,1))'.format(rowNum)
            value[5] = 'N/A'
            value[6] = 'N/A'
            value[7] = 'N/A'
        else:
            value[4] = '=GOOGLEFINANCE(CONCATENATE("TPE:", $A{}), "price")'.format(rowNum)
            value[5] = '=GOOGLEFINANCE(CONCATENATE("TPE:", $A{}), "change")'.format(rowNum)
            value[6] = '=GOOGLEFINANCE(CONCATENATE("TPE:", $A{}), "changepct") / 100'.format(rowNum)
            value[7] = '=GOOGLEFINANCE(CONCATENATE("TPE:", $A{}), "pe")'.format(rowNum)

    # 其實應該只要更新時間欄位就好，其他欄位不要再更新，但我懶的再改了，之後再說
    googlesheetService.updateSheet("工作表1", rowList)

    if msg != '':
        print("notify msg => " + msg)
        lineTool.lineNotify(os.environ["LINE_TEST_TOKEN"], msg)
    
    print('執行完畢')

    
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        lineTool.lineNotify(os.environ["LINE_TEST_TOKEN"], "notifyRockyPrice 發生錯誤")

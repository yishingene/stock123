'''
抓取 googlesheet 清單上櫃代號，抓取價格資料存到 csv 檔與更新到 googlesheet 上

Created on 2018年5月22日
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
from twse_crawler import TWSECrawler
sys.path.append("/data/data/com.termux/files/home/stock123")

# 建立 map 用來判斷該股是上市或上櫃
with open("stockIds.csv", encoding="utf-8") as f1:
    rowList = list(csv.reader(f1))
stockIdMap = {}    
for row in rowList:
    stockIdMap[row[0]] = row[4] # stockId : 上市/上櫃
    
# 所有的上櫃代號
otcStockIdNameMap = {}


def main():
    print("執行時間 {}".format(datetime.datetime.now().strftime('%Y/%m%d %H:%M:%S')))

    sheetDataList = [
        ["1F3cT6ltHQ7gOYxCPSrPJGvMpUt3b5mRJIMR0gJ5ITr8", "觀察清單", os.environ["LINE_TEST_TOKEN"]],
        ["1aveGtt653D4freXOyDkIAPbuZ5Bmw7pd-eS1JfUH9F4", "觀察清單", os.environ["LINE_REGINA_TOKEN"]],
        ["1xgtt4xjZh4Nsg6_uQnuphIbMLrBSLM-0OsOuz93NZAc", "工作表1", os.environ["LINE_PING_TOKEN"]],
        
    ]
    
    # 抓取出所有的上櫃資料到 otcStockIdNameMap
    for sheetData in sheetDataList:
        processSheet(sheetData[0], sheetData[1])

    print(otcStockIdNameMap)
    
    cnt = 0
    for stockId in otcStockIdNameMap.keys():
        cnt += 1
#         if cnt >=3:
#             continue # for test, don't want run too long
        cr = TWSECrawler()    
        js = cr.crawlStockInfoOtc(stockId)
        
        
        if js['rtcode'] == '0000' and js["rtmessage"] != "OK":
            print("查詢正確，但似乎無資料，等待 5 秒後再重新查詢一次...")
            time.sleep(5)
            js = cr.crawlStockInfoOtc(stockId)
            print(js)
            
        if js['rtcode'] == '0000' and js["rtmessage"] != "OK":
            print("查詢正確，但似乎無資料，等待 5 秒後再重新查詢一次...")
            time.sleep(5)
            js = cr.crawlStockInfoOtc(stockId)
            print(js)
        
        name = js["msgArray"][0]["n"]
        nowPrice = js["msgArray"][0].get("z", "")
        yesPrice = js["msgArray"][0].get("y", "")
        volume = js["msgArray"][0].get("v", "")
        
        print(stockId, name, nowPrice, yesPrice, volume)

        if nowPrice != "" and yesPrice != "":
            change = round(float(nowPrice) - float(yesPrice), 2)
            changepct = round(change / float(yesPrice), 4) 
            row = [stockId, name, nowPrice, change, changepct, volume]
            print(row)
            otcStockIdNameMap[stockId] = row
            
        time.sleep(5)
        
    print(otcStockIdNameMap)
    
    for sheetData in sheetDataList:
        updateSheet(sheetData[0], sheetData[1])
    
    print('執行完畢')


def processSheet(sheetId, sheetName):

    googlesheetService = GooglesheetService(sheetId)
    
    rowNum = 0    
    for value in googlesheetService.getValues(sheetName):
        rowNum += 1
        
        # header
        if rowNum == 1:
            value[10] = datetime.datetime.now().strftime('%m%d %H:%M:%S') + " OTC Updated"
            continue # header 不繼續下面的邏輯
        
        if len(value) == 0:
            continue # 略過空白行

        if stockIdMap[value[0]] == "上櫃":
            print("put {} in".format(value[0]))
            otcStockIdNameMap[value[0]] = None # 本來是想放名稱，但這裡沒有

    print("process {}/{} completed.".format(sheetId, sheetName))
    

def updateSheet(sheetId, sheetName):    
    
    googlesheetService = GooglesheetService(sheetId)
    
    rowNum = 0
    rowList = []
    for value in googlesheetService.getValues(sheetName):
        rowNum += 1
        rowList.append(value)
        
        # header
        if rowNum == 1:
            value[10] = datetime.datetime.now().strftime('%m%d %H:%M:%S') + " OTC Updated"
            continue # header 不繼續下面的邏輯
        
        if len(value) == 0:
            continue # 略過空白行

        if stockIdMap[value[0]] == "上櫃":
            row = otcStockIdNameMap[value[0]]
            if row != None:
                value[3] = '=(E{}-C{})/C{}'.format(rowNum, rowNum, rowNum)
                value[4] = row[2] # 現價
                value[5] = row[3] # 漲跌
                value[6] = row[4] # 漲跌幅度
                value[7] = row[5] # 成交量
        else:
            value[3] = '=(E{}-C{})/C{}'.format(rowNum, rowNum, rowNum)
            value[4] = '=GOOGLEFINANCE(CONCATENATE("TPE:", $A{}), "price")'.format(rowNum)
            value[5] = '=GOOGLEFINANCE(CONCATENATE("TPE:", $A{}), "change")'.format(rowNum)
            value[6] = '=GOOGLEFINANCE(CONCATENATE("TPE:", $A{}), "changepct") / 100'.format(rowNum)
            value[7] = '=GOOGLEFINANCE(CONCATENATE("TPE:", $A{}), "volume") / 1000'.format(rowNum)
            value[8] = '=GOOGLEFINANCE(CONCATENATE("TPE:", $A{}), "pe")'.format(rowNum)
                
    googlesheetService.updateSheet(sheetName, rowList)

    print("process {}/{} completed.".format(sheetId, sheetName))
    
        
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        lineTool.lineNotify(os.environ["LINE_TEST_TOKEN"], "fetchMyOtcPrice 發生錯誤")

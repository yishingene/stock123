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

    sheetDataList = [
        ["1F3cT6ltHQ7gOYxCPSrPJGvMpUt3b5mRJIMR0gJ5ITr8", "觀察清單", os.environ["LINE_TEST_TOKEN"]],
        ["1aveGtt653D4freXOyDkIAPbuZ5Bmw7pd-eS1JfUH9F4", "觀察清單", os.environ["LINE_REGINA_TOKEN"]],
        ["1xgtt4xjZh4Nsg6_uQnuphIbMLrBSLM-0OsOuz93NZAc", "工作表1", os.environ["LINE_PING_TOKEN"]],
        
        ["1sV74mTvigJbBp9X5YLyjfuxFpL3z15N5hwa-f__H5Ko", "價格通知程式", os.environ["LINE_BOOKHOU_TOKEN"]], # 2 曹書豪
        
        ["1L_opWWX_JBplMA6g9NKErmsv5fzOwWLvI8nxImdqgR4", "工作表1", os.environ["LINE_KONLON_TOKEN"]], # 3 恐龍
        
        ["1eTY5L8vHgYJ9yRFfDiBTSc5ABIfvLleyhvAiqOgWag0", "觀察名單", os.environ["LINE_ZI_TOKEN"]], # 4 謝正誠
        
        ["1bgoMruYi1dxc_tkCmwHxt1cUVm2vs-YABi3IYkOFGO0", "YuWei 股票通知", os.environ["LINE_YUWEI_TOKEN"]], # 5 YuWei
        
        ["12bdseu3Kfb2VqQSU39UmeGds9vA-8H6vOHImRiuRXuA", "觀察股", os.environ["LINE_ACELIN_TOKEN"]], # 6 Ace Lin
        
        ["1D6Z_7hJeZZTXEh-Rtx1dcBKsrk3pc61p6q4DP04Xj_E", "money", os.environ["LINE_LISA_TOKEN"]], # 7 lisa

        ["15lGfiP5F4bBVNLXGlLMj5A2EZsU209LVUp62306Nldc", "存股", os.environ["LINE_ZS_TOKEN"]], # 8 政憲
        
        ["102BsWD5WGlGeZt2ia2hJiT4najF1VfrFmuhaFfVofsc", "工作表1", os.environ["LINE_MAGGIECHOU_TOKEN"]], # 11 maggie chou
        
        ["1IW2j5I40uYgoaH2wrElEV81cqsFj7Ft-I_CB0D7aa_w", "股票報價通知", os.environ["LINE_CHARIES_TOKEN"]], # 12 charies
        
        ["1JXf1rSg8dsI09m8yy6CBFPOFydfiAnza-v-T705GCsE", "工作表1", os.environ["LINE_TINA_TOKEN"]], # 13 Tina
    ]
    
    for sheetData in sheetDataList:
        processSheet(sheetData[0], sheetData[1], sheetData[2])

    print('執行完畢')


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
            columnNum = len(value) # 取 header 的總 column 數
            value[10] = datetime.datetime.now().strftime('%m%d %H:%M:%S')
            continue # header 不繼續下面的邏輯
        
        if len(value) == 0:
            continue # 略過空白行
        # 明細列若欄位不足，先補齊，避免 exception 發生
        if len(value) < columnNum:
            for i in range(columnNum - len(value)):
                value.append("")

        # 開始比價
        try:
            nowPrice = float(value[4])
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
        print("notify msg => " + msg)
        lineTool.lineNotify(notifyLineToken, msg)
        time.sleep(1)
        
    print("process {}/{}/{} completed.".format(sheetId, sheetName, notifyLineToken))
    
    
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        lineTool.lineNotify(os.environ["LINE_TEST_TOKEN"], "notifyRockyPrice 發生錯誤")

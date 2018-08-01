'''
Created on 2018年7月10日
@author: rocky.wang
'''
import sys
sys.path.append("/data/data/com.termux/files/home/stock123")
sys.path.append("/data/data/com.termux/files/home/stock123/latestNews")

import csv
import requests
from bs4 import BeautifulSoup
import traceback
import lineTool
import os
import time
from googleService import GooglesheetService

# for test
def main1():

#     googlesheetService = GooglesheetService("1F3cT6ltHQ7gOYxCPSrPJGvMpUt3b5mRJIMR0gJ5ITr8")
#     rowList = googlesheetService.getValues("新聞通知清單")
    
    # 平大
#     googlesheetService = GooglesheetService("1xgtt4xjZh4Nsg6_uQnuphIbMLrBSLM-0OsOuz93NZAc")
#     rowList = googlesheetService.getValues("新聞通知清單")
    

    # 雪人
#     googlesheetService = GooglesheetService("1u5QaL_uyfXhom9iHVMXF1mX8D-Ssdc3zOSGFeS-Z5tk")
#     rowList = googlesheetService.getValues("新聞通知清單")
    pass
    
    
    
def main():
    
    keyExistList = []
    with open("news.csv", "r", encoding="utf-8") as f1:
        csvRowList = list(csv.reader(f1))
        for csvRow in csvRowList:
            key = csvRow[0] + csvRow[1] + csvRow[2] + csvRow[3] + csvRow[4] # 以「代號」「名稱」「日期」「時間」「標題」組合起來一起當 key
            keyExistList.append(key)
    
    # 抓取最新消息資料
    rowList = fetchNewsList()
    if len(rowList) == 0:
        print("no data found, stop to run")
        return
    
    for row in rowList:
        key = row[0] + row[1] + row[2] + row[3] + row[4] # 以「代號」「名稱」「日期」「時間」「標題」組合起來一起當 key
        if key in keyExistList:
            continue
        
        # 抓取每則消息的內容明細資料
        content = fetchDetail(row[5])
        row[5] = content # 把 onclickValue 替換成 content
        print(row)
        csvRowList.append(row)
        time.sleep(5)
    
    # 寫回 csv 檔
    with open("news.csv", "w", encoding="utf-8", newline="") as f1:
        csv.writer(f1).writerows(csvRowList)
        
    processNotifyNews()
        

def fetchNewsList():
    url = "http://mops.twse.com.tw/mops/web/t05sr01_1"
    r = requests.get(url)
    r.encoding = "utf-8"
    
    soup = BeautifulSoup(r.text, "html.parser")
    
    tb = soup.find("table", {"class": "hasBorder"})
    if tb == None and "資料庫中查無需求資料" in r.text:
        return []
    
    rowList = []
    for tr in soup.find("table", {"class": "hasBorder"}).findAll("tr"):
        
        if tr.get("class")[0] == 'tblHead':
            continue # ignore header
        
        tds = tr.findAll("td")
        
        sid = tds[0].text
        sname = tds[1].text
        sdate = tds[2].text
        stime = tds[3].text
        stitle = tds[4].text.replace("\r\n", " ")
        onclickValue = tds[5].find('input').get("onclick")
        
        row = [sid, sname, sdate, stime, stitle, onclickValue, "W"] # last element means status is WAIT to be process (maybe notify people) 
        rowList.append(row)
    
    return rowList

def fetchDetail(onclickValue):
    
    postData = { 'TYPEK' : 'all', 'step' : '1' }
    
    for co in onclickValue.split(";"):
        if not co.startswith("document.fm_t05sr01_1"):
            continue
        co = co.replace("document.fm_t05sr01_1.", "").replace(".value", "").replace("'", "")
        postData[co.split("=")[0]] = co.split("=")[1]

    url = "http://mops.twse.com.tw/mops/web/ajax_t05sr01_1"
        
    r = requests.post(url, data = postData)
    r.encoding = "utf-8"
    
    soup = BeautifulSoup(r.text, "html.parser")
    td = soup.find("td", {"style": "!important;text-align:left; !important;"})
    try:
        return td.text
    except:
        return ""

def processNotifyNews():

#     sheetDataList = fetchAllSheetDataListFromMyGooglehseet()

    notifySidList = []
    pingNotifySidList = []
    sharonNotifySidList = []
    # maybe fetch googlesheet
    googlesheetService = GooglesheetService("1F3cT6ltHQ7gOYxCPSrPJGvMpUt3b5mRJIMR0gJ5ITr8")
    rowList = googlesheetService.getValues("新聞通知清單")
    
    for row in rowList:
        if len(row) == 0 or row[0] == '' and row[1] == '':
            continue # 略過空白行
        notifySidList.append(row[0])
    print(notifySidList)
    
    # 平大
    time.sleep(2)
    googlesheetService = GooglesheetService("1xgtt4xjZh4Nsg6_uQnuphIbMLrBSLM-0OsOuz93NZAc")
    pingRowList = googlesheetService.getValues("新聞通知清單")
    for row in pingRowList:
        if len(row) == 0 or row[0] == '' and row[1] == '':
            continue # 略過空白行
        pingNotifySidList.append(row[0])
    print(pingNotifySidList)
    
    # 雪人未新增
        
    
    with open("news.csv", "r", encoding="utf-8") as f1:
        csvRowList = list(csv.reader(f1))
        for csvRow in csvRowList:
            msg = "{} {} {} {} {}\n\n{}".format(csvRow[0], csvRow[1], csvRow[2], csvRow[3], csvRow[4], csvRow[5])
            if csvRow[0] in notifySidList and csvRow[6] == "W":
                lineTool.lineNotify(os.environ["LINE_TEST_TOKEN"], msg)
                
            if csvRow[0] in pingNotifySidList and csvRow[6] == "W":
                lineTool.lineNotify(os.environ["LINE_PING_TOKEN"], msg)
            
            if csvRow[0] in sharonNotifySidList and csvRow[6] == "W":
                lineTool.lineNotify(os.environ["LINE_SHARON_TOKEN"], msg)
                
            csvRow[6] = "Done"

    # 寫回 csv 檔
    with open("news.csv", "w", encoding="utf-8", newline="") as f1:
        csv.writer(f1).writerows(csvRowList)


'''
從我的 Google Sheet 抓取要掃的清單
'''
# def fetchAllSheetDataListFromMyGooglehseet():
#     
#     googlesheetService = GooglesheetService("1F3cT6ltHQ7gOYxCPSrPJGvMpUt3b5mRJIMR0gJ5ITr8")
#     rowList = googlesheetService.getValues("掃描清單")
#     rowNum = 0
#     sheetDataList = []
#     for row in rowList:
#         rowNum += 1
#         if rowNum == 1:
#             continue
#         if len(row) == 0 or row[0] == '' and row[1] == '':
#             continue # 略過空白行
#         
#         sheetId = row[1].replace("https://docs.google.com/spreadsheets/d/", "").split("/")[0]
#         # name, sheetId, token, rangeName
#         sheetDataList.append([row[0], sheetId, row[2], row[3]])
#         
#     return sheetDataList


if __name__ == "__main__":
    try:
        main()
    except:
        traceback.print_exc()
        lineTool.lineNotify(os.environ["LINE_TEST_TOKEN"], "readNews error")
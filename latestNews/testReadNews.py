'''
Created on 2018年7月10日
@author: rocky.wang
'''
import csv
import requests
from bs4 import BeautifulSoup
import traceback
import lineTool
import os
import time
import re

def main():
    
    keyExistList = []
    with open("news.csv", "r", encoding="utf-8") as f1:
        csvRowList = list(csv.reader(f1))
        for csvRow in csvRowList:
            key = csvRow[0] + csvRow[1] + csvRow[2] + csvRow[3] + csvRow[4] # 以「代號」「名稱」「日期」「時間」「標題」組合起來一起當 key
            keyExistList.append(key)
    
    # 抓取列表資料
    for row in fetchNewsList():
        key = row[0] + row[1] + row[2] + row[3] + row[4] # 以「代號」「名稱」「日期」「時間」「標題」組合起來一起當 key
        if key in keyExistList:
            continue
        
        # 抓取明細資料
        
    
        time.sleep(3)
    

def fetchNewsList():
    url = "http://mops.twse.com.tw/mops/web/t05sr01_1"
    r = requests.get(url)
    r.encoding = "utf-8"
    
    soup = BeautifulSoup(r.text, "html.parser")
    
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
        rowList.append([sid, sname, sdate, stime, stitle])
    
    return rowList

def fetchNewsDetail():
    
    pass


def getPostValus(txt, key, default = '') :

    for row in txt.split(';'):

        mo = re.match('^document\.(.*)\.(.*).value=\'(.*)\'$', row.strip())

        if not mo : 
            return default
        if mo.group(2) == key : 
            return mo.group(3)

    return default 

if __name__ == "__main__":
    try:
        main()
    except:
        traceback.print_exc()
        lineTool.lineNotify(os.environ["LINE_TEST_TOKEN"], "testReadNews error")
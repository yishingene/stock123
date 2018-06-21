'''
Created on 2018年4月18日
@author: rocky
'''
import requests
from bs4 import BeautifulSoup
import csv
import time

rowList = []

def main():
    
    try:
        url = 'http://isin.twse.com.tw/isin/C_public.jsp?strMode=2'
        fetch(url)
    except:
        print("fetch again 1")
        time.sleep(5)
        fetch(url)
        
    print(len(rowList))
    
    try:
        url = 'http://isin.twse.com.tw/isin/C_public.jsp?strMode=4'
        fetch(url)
    except:
        print("fetch again 2")
        time.sleep(5)
        fetch(url)
    
    print(len(rowList))
    
    with open("stockIds.csv", "w", newline="", encoding="utf-8") as f1:
        for row in rowList:
            csv.writer(f1).writerow(row)


def fetch(url):

    resp = requests.get(url)
    
    soup = BeautifulSoup(resp.text, "html.parser")
    
    for tr in soup.find("table", {"class": "h4"}).findAll("tr"):
        tdList = tr.findAll("td")
        # 過濾掉不是明細的 tr
        if tdList[0].text.strip() == '有價證券代號及名稱' or tdList[0].get("colspan") != None:
            continue
        
        sid = tdList[0].text.strip().split("　")[0].strip()
        sname = tdList[0].text.strip().split("　")[1].strip()
        isinCode = tdList[1].text.strip()
        onDate = tdList[2].text.strip()
        marketType = tdList[3].text.strip()
        saleCode = tdList[4].text.strip()
        cfiCode = tdList[5].text.strip()
        
        row = [sid, sname, isinCode, onDate, marketType, saleCode, cfiCode]
        rowList.append(row)


if __name__ == '__main__':
    main()        
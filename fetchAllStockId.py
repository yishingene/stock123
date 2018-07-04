'''
Created on 2018年4月18日
@author: rocky
'''
import requests
from bs4 import BeautifulSoup
import csv
import time
import lineTool
import os
import traceback


def main():
    
    rowList = []
    
    url = "http://isin.twse.com.tw/isin/C_public.jsp?strMode=2"
    rList = fetch(url)
    rowList.extend(rList)
    print("上市數量 {}".format(len(rList)))
    time.sleep(3) # 實測連抓四個不會被擋，但還是保守起見
    
    url = "http://isin.twse.com.tw/isin/C_public.jsp?strMode=4"
    rList = fetch(url)
    rowList.extend(rList)
    print("上櫃數量 {}".format(len(rList)))
    time.sleep(3) # 實測連抓四個不會被擋，但還是保守起見
    
    url = "http://isin.twse.com.tw/isin/C_public.jsp?strMode=5"
    rList = fetch(url)
    rowList.extend(rList)
    print("興櫃數量 {}".format(len(rList)))
    time.sleep(3) # 實測連抓四個不會被擋，但還是保守起見
    
    url = "http://isin.twse.com.tw/isin/C_public.jsp?strMode=1"
    rList = fetch(url)
    # 因為公開發行少了一個欄位，自己補上
    for row in rList:
        row.insert(4, "公開發行")
    rowList.extend(rList)
    print("公開發行 {}".format(len(rList)))
    time.sleep(3) # 實測連抓四個不會被擋，但還是保守起見
    
    with open("stockIds.csv", "w", newline="", encoding="utf-8") as f1:
        for row in rowList:
            csv.writer(f1).writerow(row)
    
    print("completed")

def fetch(url):

    print("fetch " + url)
    try:
        resp = requests.get(url)
    except:
        print("fetch again " + url)
        time.sleep(5)
        resp = requests.get(url)
    
    soup = BeautifulSoup(resp.text, "html.parser")
    
    rowList = []
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
    
    return rowList


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        msg = traceback.format_exc()
        lineTool.lineNotify(os.environ["LINE_TEST_TOKEN"], msg)
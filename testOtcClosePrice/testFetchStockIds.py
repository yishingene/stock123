'''
因為我想驗證一下上市的資料

Created on 2018年8月20日
@author: rocky.wang
'''
'''
Created on 2018年4月18日
@author: rocky
'''
import requests
from bs4 import BeautifulSoup
import time
import lineTool
import os
import traceback


def main():
    
    url = "http://isin.twse.com.tw/isin/C_public.jsp?strMode=2"
    rList = fetch(url)
    print("上市數量 {}".format(len(rList))) # 15611 筆，應該是還含權證什麼的
    
    # 當只有 ESVUFR 時是 919 筆，加上 CEOGEU (0050) 後有 971 筆，但還是與抓上市盤後價格資料 1064 筆不對
    # 不過這也沒什麼意義，看起來以 1064 筆為主應該就夠了
    cnt = 0
    for r in rList:
#         print(r)
        if r[6] == 'ESVUFR' or r[6] == 'CEOGEU':
            cnt += 1
    
    print(cnt)
    

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
'''
抓取銀行/保險/金控成份股
https://www.taifex.com.tw/chinese/2/9_7_3.asp

Created on 2018年3月2日
@author: rocky.wang
'''
import csv, requests
from bs4 import BeautifulSoup

def fetch():
    
    url = "https://www.taifex.com.tw/chinese/2/9_7_3.asp"
    r = requests.get(url)
    r.encoding = "utf-8"
     
    soup = BeautifulSoup(r.text, "html.parser")
    tb = soup.find("table", {"class": "table_c"})
    
    rowList = []
    rowList2 = [] # 為了排序問題
    # 這裡的格式比較特別是一行 tr 可能有兩個代號與比重
    for tr in tb.findAll("tr", {"valign": "bottom"}):
        tds = tr.findAll("td")
        row = [tds[1].text.strip(), tds[2].text.strip(), tds[3].text.strip()]
        rowList.append(row)
        
        # 如果第五欄(流水號)還有資料，代表還有另一筆
        if tds[4].text.strip() != '':
            row = [tds[5].text.strip(), tds[6].text.strip(), tds[7].text.strip()]
            rowList2.append(row)

    # 因為 rowList2 的佔比較少，後面才加回去，讓排序是由大到小
    for row in rowList2:
        rowList.append(row)
    
    for row in rowList:
        print(row)
    print("共 {} 筆資料".format(len(rowList)))
    
     
fetch()
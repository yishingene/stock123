'''
抓取元大 ETF 成份股資料
http://www.yuantaetfs.com/#/Orders/1066 (0050)

Created on 2018年3月2日
@author: rocky.wang
'''
import csv, requests
import datetime
from bs4 import BeautifulSoup

"""
抓取元大ETF成份股
"""
def fetch(fundId, sid):
    
    url = "http://www.yuantaetfs.com/api/Composition?date={}&fundid={}".format(datetime.datetime.now().strftime('%Y%m%d'), fundId)
    r = requests.get(url)
    js = r.json()
    print(js)
     
    with open("{}composition.csv".format(sid), "w", newline="\n", encoding="utf-8") as f1:
        writer = csv.writer(f1)
        for i in range(len(js)):
            writer.writerow([js[i].get("stkcd"), js[i].get("name"), js[i].get("ename"), js[i].get("qty"), js[i].get("cashinlieu"), js[i].get("minimum")])
            

"""
抓取兆豐00690ETF成份股
"""
def fetch00690():
    
    url = "https://www.megafunds.com.tw/ETF/product/fundshares.aspx?nid=5"
    
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    tb = soup.findAll("table", {"class": "tb-vertical"})[1]
    
    rowNum = -1
    for tr in tb.findAll("tr"):
        rowNum += 1
        if rowNum == 0:
            continue # 表頭
    
        tds = tr.findAll("td")
        row = [tds[0].text, tds[1].text.strip(), tds[2].text, tds[3].text]
        print(row)
        


# fetch("1066", "0050")
# 
# fetch("1078", "0051")    

fetch00690()

'''
Created on 2018年7月7日
@author: rocky.wang
'''
import requests
from bs4 import BeautifulSoup

def fetch():
    url = "http://mops.twse.com.tw/mops/web/t05sr01_1"
    r = requests.get(url)
    r.encoding = "utf-8"
#     print(r.text)
    
    
    soup = BeautifulSoup(r.text, "html.parser")
    
    table = soup.find("table", {"class": "hasBorder"})
    
    for tr in table.findAll("tr"):
        if tr.get("class")[0] == 'tblHead':
            continue
        
        tds = tr.findAll("td")
        
        sid = tds[0].text
        sname = tds[1].text
        title = tds[4].text
        
        print(sid, sname, title)
        print("--------------------")
    
fetch()
'''
test detail

Created on 2018年7月7日
@author: rocky.wang
'''
import requests
import time 
import re 
from bs4 import BeautifulSoup
import csv

def getPostValus(txt, key, default = '') :

    for row in txt.split(';'):

        mo = re.match('^document\.(.*)\.(.*).value=\'(.*)\'$', row.strip())

        if not mo : 
            return default
        if mo.group(2) == key : 
            return mo.group(3)

    return default 


def fetch():
    url = "http://mops.twse.com.tw/mops/web/t05sr01_1"
    r = requests.get(url)
    r.encoding = "utf-8"
    
    soup = BeautifulSoup(r.text, "html.parser")
    
    table = soup.find("table", {"class": "hasBorder"})
    
    rowList = []
    for tr in table.findAll("tr"):
        if tr.get("class")[0] == 'tblHead':
            continue
        
        tds = tr.findAll("td")
        
        sid = tds[0].text
        sname = tds[1].text
        sdate = tds[2].text
        stime = tds[3].text
        title = tds[4].text
        
#         print(sid, sname, sdate, stime, title)

        detailUrl = "http://mops.twse.com.tw/mops/web/ajax_t05sr01_1"
        postData = composePostData(tds[5].find('input').get("onclick"))
        
        r = requests.post(detailUrl, data = postData)
        r.encoding = "utf-8"
 
        soup = BeautifulSoup(r.text, "html.parser")
        td = soup.find("td", {"style": "!important;text-align:left; !important;"})
        print(td.text)
         
        row = [sid, sname, sdate, stime, title, td.text]
        rowList.append(row)
    
        break

def composePostData(onclickValue):
    
    postData = {
        'TYPEK' : 'all', 
        'step' : '1'
    }
        
    for co in onclickValue.split(";"):
        if not co.startswith("document.fm_t05sr01_1"):
            continue
        co = co.replace("document.fm_t05sr01_1.", "").replace(".value", "").replace("'", "")
        postData[co.split("=")[0]] = co.split("=")[1]
    
    return postData
    
fetch()

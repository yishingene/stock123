# -*- coding: utf-8 -*-

'''
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
        
        print(sid, sname, sdate, stime, title)

        txt = tds[5].find('input')

        headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
                'Referer' : url
        }

        post_url = 'http://mops.twse.com.tw/mops/web/ajax_t05sr01_1'
        postData = {
                'TYPEK' : 'all', 
                'step' : '1' ,
                'skey' : getPostValus(txt.get('onclick'), 'skey' ),
                'hhc_co_name' : getPostValus(txt.get('onclick'), 'hhc_co_name' ),
                'COMPANY_ID' : getPostValus(txt.get('onclick'), 'COMPANY_ID' ),
                'COMPANY_NAME' : getPostValus(txt.get('onclick'), 'COMPANY_NAME' ),
                'SPOKE_DATE' : getPostValus(txt.get('onclick'), 'SPOKE_DATE' ),
                'SPOKE_TIME' : getPostValus(txt.get('onclick'), 'SPOKE_TIME' ),
                'SEQ_NO' : getPostValus(txt.get('onclick'), 'SEQ_NO' ),
        }

        r = requests.post(post_url, data = postData, headers = headers)
        r.encoding = "utf-8"

        soup = BeautifulSoup(r.text, "html.parser")
        td = soup.find("td", {"style": "!important;text-align:left; !important;"})
        print(td.text)
        
        row = [sid, sname, sdate, stime, title, td.text]
        rowList.append(row)
        
        time.sleep(3)
    
    with open("news.csv", "w", encoding="utf-8", newline="") as f1:
        writer = csv.writer(f1)
        writer.writerows(rowList)    
        
fetch()

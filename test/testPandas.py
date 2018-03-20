'''
Created on 2018年3月20日
@author: rocky.wang
'''
import requests

import pandas as pd
from bs4 import BeautifulSoup

url = 'https://goodinfo.tw/StockInfo/StockDividendScheduleList.asp?MARKET_CAT=%E5%85%A8%E9%83%A8&INDUSTRY_CAT=%E5%85%A8%E9%83%A8&YEAR=2017'
# table = pd.read_html(url)[0]
# # table = table.drop(table.columns[[0,1,2,3,4]],axis=0)
# # table = table.drop(table.columns[9:296],axis=1)
# print(table)

if __name__ == "__main__":
    headers = { 'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36',
                    'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                }
    
    url = "https://goodinfo.tw/StockInfo/StockDividendScheduleList.asp?MARKET_CAT=%E5%85%A8%E9%83%A8&INDUSTRY_CAT=%E5%85%A8%E9%83%A8&YEAR=2017"
    
    resp = requests.get(url, headers=headers)
    resp.encoding = "utf-8"
    
    soup = BeautifulSoup(resp.text, "html.parser")
    
#     div = soup.findAll("table", {"class": "solid_1_padding_3_2_tbl", "bgcolor": "#d7e6f4"})
    
    div = soup.findAll("a", {"class": "link_black"})
    
    print(len(div))
    
    for d in div:
        print(d)
    
    
    
    
    

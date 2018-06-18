'''
Created on 2018年6月6日
@author: Rocky
'''
import requests
from bs4 import BeautifulSoup
import re

def main():
        
    url = "https://goodinfo.tw/StockInfo/StockList.asp?SEARCH_WORD=&SHEET=%E5%AD%A3%E7%8D%B2%E5%88%A9%E8%83%BD%E5%8A%9B&MARKET_CAT=%E6%99%BA%E6%85%A7%E9%81%B8%E8%82%A1&INDUSTRY_CAT=%E4%B8%89%E5%A4%A7%E6%B3%95%E4%BA%BA%E9%80%A3%E8%B2%B7+%28%E6%97%A5%29%40%40%E4%B8%89%E5%A4%A7%E6%B3%95%E4%BA%BA%E9%80%A3%E7%BA%8C%E8%B2%B7%E8%B6%85%40%40%E9%80%A3%E7%BA%8C%E8%B2%B7%E8%B6%85+%28%E6%97%A5%29&STOCK_CODE=&RANK=0&STEP=DATA&SHEET2=%E7%8D%B2%E5%88%A9%E8%83%BD%E5%8A%9B%20(%E5%AD%A3%E5%A2%9E%E6%B8%9B%E7%B5%B1%E8%A8%88)&RPT_TIME=20174"
    
    headers = {
        "User-Agent" : "Chrome/31.0.1650.63",
        "referer": "https://goodinfo.tw/StockInfo/StockList.asp?MARKET_CAT=%E6%99%BA%E6%85%A7%E9%81%B8%E8%82%A1&INDUSTRY_CAT=%E4%B8%89%E5%A4%A7%E6%B3%95%E4%BA%BA%E9%80%A3%E8%B2%B7+%28%E6%97%A5%29&SHEET=%E6%B3%95%E4%BA%BA%E8%B2%B7%E8%B3%A3&SHEET2=%E9%80%A3%E8%B2%B7%E9%80%A3%E8%B3%A3%E7%B5%B1%E8%A8%88%28%E6%97%A5%29"
    }
    
    r = requests.post(url, headers=headers)
    r.encoding = "utf-8"
    
    soup = BeautifulSoup(r.text, "html.parser")
    trs = soup.findAll("tr", id=re.compile("^row"))
    
    for tr in trs:
        print(tr)


if __name__ == "__main__":
    main()
    
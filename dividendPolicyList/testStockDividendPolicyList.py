'''
Created on 2018年6月8日
@author: rocky.wang
'''
import requests
from bs4 import BeautifulSoup
import re, csv

def main():
    fetch()

# https://goodinfo.tw/StockInfo/StockDividendPolicy.asp?STOCK_ID=1215

def fetch():

    marketCat = '上市'
    industryCat = '食品工業'
    year = "2016"
    url = "https://goodinfo.tw/StockInfo/StockDividendPolicyList.asp?MARKET_CAT={}&INDUSTRY_CAT={}&YEAR={}".format(marketCat, industryCat, year)
    
    headers = {
        "User-Agent" : "Chrome/66.0.3359.181", 
    }
    r = requests.get(url, headers=headers)
    r.encoding = "utf-8"
    soup = BeautifulSoup(r.text, "html.parser")
    trList = soup.findAll("tr", id=re.compile("^row"))
    
    rowList = []
    for tr in trList:
        row = []
        for td in tr.findAll("td"):
            row.append(td.text)
        print(row)
        rowList.append(row)
        
    with open("dividend_{}.csv".format(year), "w", enconding="utf-8") as f1:
        cw = csv.writer(f1)
        

if __name__ == "__main__":
    main()

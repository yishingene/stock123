'''
抓取稅後淨利

Created on 2018年4月8日
@author: rocky.wang
'''
import requests

from bs4 import BeautifulSoup
import re


def main():
    stockId = "1264"
    pureEarn = fetchStockBzPerformance(stockId)
    print(pureEarn)

def fetchStockBzPerformance(stockId):
    
    url = "https://goodinfo.tw/StockInfo/StockBzPerformance.asp?STOCK_ID={}".format(stockId)
    resp = requests.get(url, headers={"User-Agent" : "Chrome/31.0.1650.63"})
    resp.encoding = "utf-8"
    
    soup = BeautifulSoup(resp.text, "html.parser")
    table = soup.find("table", {"class": "solid_1_padding_3_0_tbl", "style": "font-size:10pt;line-height:16px;"})
    trList = table.findAll("tr", id=re.compile("^row"))
    
    # 最新一年的稅後淨利
    pureEarn = trList[0].findAll("td")[11].text.strip().replace(",", "")
    return float(pureEarn)

if __name__ == "__main__":
    main()
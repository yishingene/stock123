'''
抓取長期負債金額

網址 https://goodinfo.tw/StockInfo/StockAssetsStatus.asp?STOCK_ID=1264
但還需下拉至「資產負債金額」 

Created on 2018年4月8日
@author: rocky.wang
'''
import requests
from bs4 import BeautifulSoup
import re

def main():
    stockId = "1264"
    longTermDebit = fetchStockAssetsStatus(stockId)
    print(longTermDebit)


def fetchStockAssetsStatus(stockId):

    url = "https://goodinfo.tw/StockInfo/StockAssetsStatus.asp"
    
    # 其實重點只有 referer & User-Agent 一定要有
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6",
        "content-length": "0",
        "content-type": "application/x-www-form-urlencoded;",
        "cookie": "_ga=GA1.2.972014549.1521094387; __gads=ID=37c2713320da8907:T=1521094373:S=ALNI_MYyJzHXZ-jBZmWU8NUcnypNT34Dbw; SCREEN_SIZE=WIDTH=1536&HEIGHT=864; GOOD%5FINFO%5FSTOCK%5FBROWSE%5FLIST=1%7C6184; CLIENT%5FID=20180405213653515%5F115%2E82%2E255%2E57; _gid=GA1.2.1798244195.1524455242",
        "origin": "https://goodinfo.tw",
        "referer": "https://goodinfo.tw/StockInfo/StockAssetsStatus.asp?STOCK_ID=1264",
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36", 
    }
    data = {
        "STOCK_ID": stockId, 
        "RPT_CAT": "M_YEAR", 
        "STEP": "DATA", 
        "SHEET": "資產負債金額"
    }
    
    resp = requests.post(url, headers=headers, data=data)
    resp.encoding = "utf-8"
    
    soup = BeautifulSoup(resp.text, "html.parser")
    
    trList = soup.findAll("tr", id=re.compile("^row")) 
    
    longTermDebit = trList[0].findAll("td")[18].text.strip().replace(",", "")
    print(longTermDebit)
    
    return float(longTermDebit)


if __name__ == "__main__":
    main()

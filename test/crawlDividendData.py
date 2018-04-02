'''
crawl 2017股利年度除權息日程  (2018年發放)

https://goodinfo.tw/StockInfo/StockDividendScheduleList.asp?MARKET_CAT=全部&INDUSTRY_CAT=全部&YEAR=2017

Created on 2018年3月20日
@author: rocky.wang
'''
import requests
import re
from bs4 import BeautifulSoup
import csv
import time


def main():
    # 注意這個年度是股利所屬年度，發放是隔年
    # 1988 似乎是最後一年有資料了
#     year = 1988
#     for i in range(0, 1):
#         fetch(year-i)
#         time.sleep(10)

    fetch(2017)

def fetch(year):
    
    url = "https://goodinfo.tw/StockInfo/StockDividendScheduleList.asp?MARKET_CAT={}&INDUSTRY_CAT={}&YEAR={}".format("全部", "全部", year)
    
    url = "https://goodinfo.tw/StockInfo/StockDividendPolicyList.asp?"
    print(url)

# Pandas 這樣的寫法是可以了，但資料看起來超亂，應該是我不會用，還是先用 BeautifulSoup 就好了
#     resp = requests.get(url, headers=headers)
#     resp.encoding = "utf-8"
#     tb = pd.read_html(resp.text, header=0, attrs={"width": "100%", "style": "font-size: 9pt"})
#     print(tb)

    resp = requests.get(url, headers={"User-Agent" : "Chrome/31.0.1650.63"})
    resp.encoding = "utf-8"
    soup = BeautifulSoup(resp.text, "html.parser")
    trs = soup.findAll("tr", id=re.compile("^row"))
    
    rowList = []
    for tr in trs:
        row = [td.text.strip("\xa0") for td in tr.findAll("td")]
        rowList.append(row)
        
    with open("{}dividend.csv".format(year), "w", encoding="utf-8", newline="") as f1:
        csv.writer(f1, delimiter="\t").writerows(rowList)
    
    print("completed")

    
if __name__ == "__main__":
    main()

'''
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
    
    headers = { 'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36',
                    'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                }
    url = "https://goodinfo.tw/StockInfo/StockDividendScheduleList.asp?MARKET_CAT={}&INDUSTRY_CAT={}&YEAR={}".format("全部", "全部", year)
    print(url)

# Pandas 這樣的寫法是可以了，但資料看起來超亂，應該是我不會用，還是先用 BeautifulSoup 就好了
#     resp = requests.get(url, headers=headers)
#     resp.encoding = "utf-8"
#     tb = pd.read_html(resp.text, header=0, attrs={"width": "100%", "style": "font-size: 9pt"})
#     print(tb)

    resp = requests.get(url, headers=headers)
    resp.encoding = "utf-8"
    soup = BeautifulSoup(resp.text, "html.parser")
    trs = soup.findAll("tr", id=re.compile("^row"))
    
    rowList = []
    for tr in trs:
        row = [td.text.strip('\xa0') for td in tr.findAll("td")]
        rowList.append(row)
    
    with open("{}dividend.csv".format(year), "w", encoding="utf-8", newline="") as f1:
        writer = csv.writer(f1)
        for row in rowList:
            writer.writerow(row)
    
if __name__ == "__main__":
    main()

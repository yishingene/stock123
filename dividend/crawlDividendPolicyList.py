'''
crawl 股利一覽
https://goodinfo.tw/StockInfo/StockDividendPolicyList.asp

Created on 2018年6月9日
@author: rocky.wang
'''
import requests
import re
from bs4 import BeautifulSoup
import csv
import time


def main():
    # 注意這個年度是股利所屬年度，所以 2018 年時的值是 2017
    # 似乎跑著跑著還是可能會卡住，必須停掉再重跑
#     for year in range(1969, 2018):
#     for year in range(2004, 2007):
#         fetch("全部", "全部", year)
#         time.sleep(10)

    fetch("全部", "全部", 2017)

    # 第一次才跑上面的 for 迴圈，之後只要抓最新年度就好了 (注意是所屬年度，所以 2018 年時的值是 2017)
#     fetch("全部", "全部", "2017")

    # 測試用
    # 若用全部/全部，有時會查太久都不知道有沒有要回來，不過大概是 chrome 或其他應用程式吃飽佔著了，發現關掉 chrome 後抓取就蠻順的了
#     fetch("上市", "水泥工業", 2017)
#     fetch("上市", "全部", 2016)
#     fetch("全部", "全部", 2016)

def fetch(marketCat, industryCat, year):
    
    url = "https://goodinfo.tw/StockInfo/StockDividendPolicyList.asp?MARKET_CAT={}&INDUSTRY_CAT={}&YEAR={}".format(marketCat, industryCat, year)
    print(url)

    headers = {
        "User-Agent" : "Chrome/31.0.1650.63"
    }
    resp = requests.get(url, headers=headers)
    resp.encoding = "utf-8"
    soup = BeautifulSoup(resp.text, "html.parser")
    
    trs = soup.findAll("tr", id=re.compile("^row"))
    rowList = []
    for tr in trs:
        row = [td.text.strip("\xa0") for td in tr.findAll("td")]
        rowList.append(row)
        print(row)
    
    with open("{}stockDividendPolicyList.csv".format(year), "w", encoding="utf-8", newline="") as f1:
        csv.writer(f1).writerows(rowList)
    
    print("{} completed".format(year))


if __name__ == "__main__":
    main()

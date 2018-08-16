'''
抓取元大 ETF 成份股資料
http://www.yuantaetfs.com/#/Orders/1066 (0050)

Created on 2018年3月2日
@author: rocky.wang
'''
import csv, requests
import datetime

def fetch(fundId, sid):
    
    url = "http://www.yuantaetfs.com/api/Composition?date={}&fundid={}".format(datetime.datetime.now().strftime('%Y%m%d'), fundId)
    r = requests.get(url)
    js = r.json()
    print(js)
     
    with open("{}composition.csv".format(sid), "w", newline="\n", encoding="utf-8") as f1:
        writer = csv.writer(f1)
        for i in range(len(js)):
            writer.writerow([js[i].get("stkcd"), js[i].get("name"), js[i].get("ename"), js[i].get("qty"), js[i].get("cashinlieu"), js[i].get("minimum")])
            


fetch("1066", "0050")

fetch("1078", "0051")


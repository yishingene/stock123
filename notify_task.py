'''
Created on 2018年3月27日
@author: rocky.wang
'''

import csv
import datetime
import lineTool
import os
import sys
import time
sys.path.append("/data/data/com.termux/files/home/stock123")

def main():
    
    print("執行時間 {}".format(datetime.datetime.now().strftime('%Y/%m%d %H:%M:%S')))

    now = datetime.datetime.now()
    
    # 取最後一筆資料
    with open("data/t00.csv", encoding="MS950") as f1:
        row = list(csv.reader(f1))[-1]

    # 若日期等於今日才作通知
    if row[0] != now.strftime("%Y/%m/%d"):
        print("無今日資料，不進行通知")
        return
    
    yestPrice = float(row[6]) - float(row[7])
    pct = round(float(row[7]) / yestPrice * 100, 2)
    
    msg = "{} 大盤 K 值 {}\n\n大盤指數 {} {} ({:.2f}%)".format(row[0], row[10], row[6], row[7], pct)
    msg += "\n"
    msg += composeMsg("0050")
    msg += "\n"
    msg += composeMsg("0056")
    
    if float(row[10]) >= 80:
        msg += "\n\n## 大盤 K 值已超過 80，建議賣出 0050 ##"
    elif float(row[10]) <=20:
        msg += "\n\n## 大盤 K 值已低於 20，建議買入 0050 ##"
    
    # 0056 額外通知訊息
    with open("data/0056.csv", encoding="MS950") as f1:
        row = list(csv.reader(f1))[-1]    
    
    amt = int(row[1]) // 1000
    if amt >= 2000 and amt < 5000:
        msg += "\n\n## 0056 成交量 {} 張，較平常多，可留意是否較低價可買入 ##".format(amt)
    elif amt >= 5000 and amt < 8000:
        msg += "\n\n## 0056 成交量 {} 張，數量偏大，可留意是否較低價可買入 ##".format(amt)
    elif amt >= 8000:
        msg += "\n\n## 0056 成交量 {} 張，異常的高，請留意是否較低價可買入 ##".format(amt)
    
    k9 = float(row[10])
    if k9 <= 20:
        msg += "\n\n## 0056 K值已低於 20，可考慮低價可買入 ##".format(amt)
    elif k9 >= 80:
        msg += "\n\n## 0056 K值已高於 80，可考慮價差 1元以上賣出 ##".format(amt)
    
    print(msg)

    # 發 LINE 通知
    lineTool.lineNotify(os.environ["LINE_0050_TOKEN"], msg)
    time.sleep(2)   # delays for n seconds
    lineTool.lineNotify(os.environ["LINE_0050_TOKEN2"], msg)
    time.sleep(2)
    lineTool.lineNotify(os.environ["LINE_0050_TOKEN3"], msg)
    time.sleep(2)
    lineTool.lineNotify(os.environ["LINE_0050_TOKEN4"], msg)
    time.sleep(2)
    lineTool.lineNotify(os.environ["LINE_0050_TOKEN5"], msg)
    time.sleep(2)
    lineTool.lineNotify(os.environ["LINE_0050_TOKEN6"], msg)
    
#     lineTool.lineNotify(os.environ["LINE_TEST_TOKEN"], msg)


def composeMsg(stockId):
    
    with open("data/{}.csv".format(stockId), encoding="MS950") as f1:
        row = list(csv.reader(f1))[-1]
    
    percent = float(row[7]) / (float(row[6]) - float(row[7])) * 100 # 透過漲跌金額算出昨日金額計算幅度
    return "{}價格 {} {} ({:.2f}%)  K 值 {}".format(stockId, row[6], row[7], percent, row[10])


if __name__ == "__main__":
    main()

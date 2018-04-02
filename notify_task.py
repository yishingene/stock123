'''
Created on 2018年3月27日
@author: rocky.wang
'''

import csv
import datetime
import lineTool
import os
import sys
sys.path.append("/data/data/com.termux/files/home/stock123")

def main():

    now = datetime.datetime.now()
    
    # 取最後一筆資料
    with open("data/t00.csv", encoding="MS950") as f1:
        row = list(csv.reader(f1))[-1]

    # 若日期等於今日才作通知
#     if row[0] != now.strftime("%Y/%m/%d"):
#         print("無今日資料，不進行通知")
#         return
    
    msg = "{}大盤 K 值 {}".format(row[0], row[10])

    msg += "\n\n"
    msg += composeMsg("0050")
    msg += "\n"
    msg += composeMsg("0056")
    
    if float(row[10]) >= 80:
        msg += "\n\n## 大盤 K 值已超過 80，建議賣出 ##"
    elif float(row[10]) <=20:
        msg += "\n\n## 大盤 K 值已低於 20，建議買入 ##"
    print(msg)

    # 發 LINE 通知
#     lineTool.lineNotify(os.environ["LINE_0050_TOKEN"], msg)
#     time.sleep(2)   # delays for n seconds
#     lineTool.lineNotify(os.environ["LINE_0050_TOKEN2"], msg)
#     time.sleep(2)
#     lineTool.lineNotify(os.environ["LINE_0050_TOKEN3"], msg)
#     time.sleep(2)
#     lineTool.lineNotify(os.environ["LINE_0050_TOKEN4"], msg)
#     time.sleep(2)
#     lineTool.lineNotify(os.environ["LINE_0050_TOKEN5"], msg)
#     time.sleep(2)
#     lineTool.lineNotify(os.environ["LINE_0050_TOKEN6"], msg)
    lineTool.lineNotify(os.environ["LINE_TEST_TOKEN"], msg)


def composeMsg(stockId):
    
    with open("data/{}.csv".format(stockId), encoding="MS950") as f1:
        row = list(csv.reader(f1))[-1]
    
    percent = float(row[7]) / (float(row[6]) - float(row[7])) * 100 # 透過漲跌金額算出昨日金額計算幅度
    return "{}價格 {} {} ({:.2f}%)  K 值 {}".format(stockId, row[6], row[7], percent, row[10])


if __name__ == "__main__":
    main()

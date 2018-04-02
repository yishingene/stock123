'''
Created on 2018年3月27日
@author: rocky.wang
'''
import csv
import datetime
import lineTool
import os

def main():

    now = datetime.datetime.now()
    
    # 取最後一筆資料
    with open("data/t00.csv") as f1:
        row = list(csv.reader(f1))[-1]

    # 若日期等於今日才作通知
    if row[0] != now.strftime("%Y/%m/%d"):
        print("無今日資料，不進行通知")
        return
    
    msg = "{}大盤 K 值 {}".format(row[0], row[10])

    msg += "\n\n"
    msg += composeMsg("0050")
    msg += "\n"
    msg += composeMsg("0056")
    
    print(msg)


def composeMsg(stockId):
    
    with open("data/{}.csv".format(stockId)) as f1:
        row = list(csv.reader(f1))[-1]
    
    percent = float(row[7]) / (float(row[6]) - float(row[7])) * 100 # 透過漲跌金額算出昨日金額計算幅度
    return "{}價格 {} {} ({:.2f}%)  K 值 {}".format(stockId, row[6], row[7], percent, row[10])


if __name__ == "__main__":
    main()

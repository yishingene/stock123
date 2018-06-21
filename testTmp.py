'''
Created on 2018年6月21日
@author: rocky.wang
'''
import csv
import os


stockId = "0050xx"

if not os.path.exists("data/{}.csv".format(stockId)):
    
    print("not exist")
    
    with open("data/{}.csv".format(stockId), "a", newline="", encoding="cp950") as f1:    
        writer = csv.writer(f1)
        writer.writerow(["日期","成交股數","成交金額","開盤價","最高價","最低價","收盤價","漲跌價差","成交筆數","RSV","K9"])

with open("data/{}.csv".format(stockId), "r", encoding="cp950") as f1:
    for row1 in csv.reader(f1):
        print(row1)

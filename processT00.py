'''
Created on 2018年3月28日
@author: rocky.wang
'''
import csv

rowList = []
rowList.append(['日期', '成交股數', '成交金額', '開盤價', '最高價', '最低價', '收盤價', '漲跌價差', '成交筆數', 'RSV', 'K9'])
with open("t00.csv") as f1:
    reader = csv.reader(f1)
    next(reader)
    for row in reader:
        newRow = [row[0], '', '', row[1], row[2], row[3], row[4], '', '', row[5], row[6]]
        rowList.append(newRow)


with open("t00new.csv", "w", newline="") as f1:
    writer = csv.writer(f1)
    for row in rowList:
        writer.writerow(row)
    
    

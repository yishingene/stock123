'''
Created on 2018年3月27日
@author: rocky.wang
'''
import csv
import datetime

def main():

    now = datetime.datetime.now()
    
    # 取最後一筆資料
    with open("t00.csv") as f1:
        row = list(csv.reader(f1))[-1]

    

    # 若日期等於今日才作通知
#     if row[0] != now.strftime("%Y/%m/%d"):
#         print("無今日資料，不進行通知")
#         return
    
    msg = "{}大盤 K 值 {}".format(row[0], row[6])

    msg += "\n"
    msg += composeMsg("0050")
    msg += "\n"
    msg += composeMsg("0056")
    
    print(msg)


def composeMsg(stockId):
    
    with open("data/{}.csv".format(stockId)) as f1:
        row = list(csv.reader(f1))[-1]
    
    msg = "{}價格 {}\tK 值 {}".format(stockId, row[6], row[10])
    
#     diff = z - y
#     diffStr = "%.2f" %(diff)
#     if diff > 0:
#         diffStr = "▲" + diffStr
#         precentDiff = diff / y * 100
#         preDiffStr = "%.2f" %(precentDiff) + "%"
#         diffStr = diffStr + " (" + preDiffStr + ")"
#         msg += " " + diffStr
#     elif diff < 0:
#         diffStr = "▼" + diffStr
#         precentDiff = diff / y * 100
#         preDiffStr = "%.2f" %(precentDiff) + "%"
#         diffStr = diffStr + " (" + preDiffStr + ")"
#         msg += " " + diffStr    

    return msg

if __name__ == "__main__":
    main()

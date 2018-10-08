import traceback
import lineTool
import os
import datetime
import csv
from calendar import month


def main():

    print("執行時間 {}".format(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')))

    now = datetime.datetime.now()
    
    for i in range(3):
        now = now + datetime.timedelta(month=-1)
        print(now)
    
#     sid = "6023"
#     findOtcPriceByFile(sid)


#     sids = '00730,00731,00732,00733,00735,00736,00737,00738U,00739,00742,00743,01009T,1587,2630,2881B,2882B,2891B,3312,3530,3711,4540,4566,4989,6288,6416,6581,6625,8028,8482,8497'
#     
#     with open("stockIds.csv", "r", encoding="utf-8") as f1:
#         rowList = list(csv.reader(f1))
#     
#     sidArr = sids.split(",")
#     for sid in sidArr:
#         for row in rowList:
#             if row[0] == sid:
#                 print(row)

    pass



def findOtcPriceByFile(sid):

    now = datetime.datetime.now()
    
    for i in range(15):
        csv_reader = csv.reader(open("data_daily_close_quotes/otc_{}.csv".format(now.strftime("%Y%m%d")), "r", encoding="utf-8"))
        for row in csv_reader:
            if row[0] == sid:
                print(sid, row[1], row[2])
                return row[2]
        
        now = now + datetime.timedelta(days=-1)
    
    return None




def a(a, b):
    
    a = [0, 1, 2, 3]
    
    a.insert(1, 5)
    
    print(a)
    
#     return a / b

if __name__ == "__main__":
    main()
        
        
        
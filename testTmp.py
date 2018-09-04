import traceback
import lineTool
import os
import datetime
import csv
from matplotlib.mlab import csv2rec


def main():

    print("執行時間 {}".format(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')))

    now = datetime.datetime.now()
    
    for i in range(3):
        now = now + datetime.timedelta(days=-1)
    
    sid = "6023"
    findOtcPriceByFile(sid)

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
        
        
        
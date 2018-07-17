'''
讀取並做些動作

Created on 2018年7月17日
@author: rocky.wang
'''
import csv
import datetime
import os

def read():
    
    today = datetime.date.today()
    nextMonday = today + datetime.timedelta(days=6)
    nextSunday = nextMonday + datetime.timedelta(days=6)
    
    sNextMonday = nextMonday.strftime("%Y/%m/%d")
    sNextSunday = nextSunday.strftime("%Y/%m/%d")
    
    cnt = 0
    for name in os.listdir():
        if name.startswith("stockDividendSchedule_"):
            sid = name.split(".")[0].split("_")[1]
            with open("stockDividendSchedule_{}.csv".format(sid), "r", encoding="utf-8") as f1:
                rowList = list(csv.reader(f1))
                
                if len(rowList) == 1:
                    continue
                
                row = rowList[1]

                d1 = row[3].replace("(即將除息)", "")
                d2 = row[5].replace("(即將除權)", "")
                
                
                if (sNextMonday <= d1 <= sNextSunday) or (sNextMonday <= d2 <= sNextSunday):
                    print(sid)
                    cnt += 1
    
    print(cnt)
read()


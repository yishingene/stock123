'''
盤中即時通知 K 值

Created on 2018年4月24日
@author: rocky.wang
'''
import csv
import sys
import datetime
import traceback
import lineTool
import os
import time

sys.path.append("/data/data/com.termux/files/home/stock123")

def main():
    print("\n執行時間 {}".format(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')))
    
    dt = datetime.datetime.now().strftime('%Y/%m/%d')

    with open("data/t00.csv", encoding="MS950") as f1:
        row = list(csv.reader(f1))[-1]
    
    if row[0] != datetime.datetime.now().strftime('%Y/%m/%d'):
        print("無今日大盤資料，不繼續執行")
        return
    
    k9 = float(row[10])
    
    if k9 <= 20:
        with open("notify.csv", encoding="utf-8") as f1:
            row = list(csv.reader(f1))[-1]

        if row[0] == dt:
            print("今日已通知過，不繼續")
        else:
            with open("notify.csv", "a", newline="", encoding="utf-8") as f1:
                writer = csv.writer(f1)
                writer.writerow([dt, k9])
        
            msg = "盤中 K 值已低於 20，該出手了 !"
            print(msg)
            notifyAll(msg)
    
    elif k9 >= 80:
        with open("notify.csv", encoding="utf-8") as f1:
            row = list(csv.reader(f1))[-1]
    
        if row[0] == dt:
            print("今日已通知過，不繼續")
        else:
            with open("notify.csv", "a", newline="", encoding="utf-8") as f1:
                writer = csv.writer(f1)
                writer.writerow([dt, k9])
        
            msg = "盤中 K 值已高於 80，該出手了 !"
            print(msg)
            notifyAll(msg)
    
    else:
        print("不進行通知，目前 K 值 {}".format(k9))      
            
def notifyAll(msg):
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
    time.sleep(2)
    lineTool.lineNotify(os.environ["LINE_0050_TOKEN7"], msg)
    
#     lineTool.lineNotify(os.environ["LINE_TEST_TOKEN"], msg)
    

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        lineTool.lineNotify(os.environ["LINE_TEST_TOKEN"], "notifyT00realtime 發生錯誤")
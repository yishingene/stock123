'''
計算個股 RSA, K9 值，新增至 {stockId}withRSVK9.csv

Created on 2017年11月12日
@author: Rocky
'''
import csv
import os
import time

def main():
    t1 = time.time()
    for filename in os.listdir("data"):
        stockId = filename.split(".")[0]
        print("process stockId {}".format(stockId))
        appendData(stockId)
    
    t2 = time.time()
    
    t3 = t2 - t1
    print("spend {} seconds".format(t3))
    

def appendData(stockId):
    
    maxList = [0, 0, 0, 0, 0, 0, 0, 0, 0] # 9 天的最高價
    minList = [0, 0, 0, 0, 0, 0, 0, 0, 0] # 9 天的最低價
    k9 = 50
    cnt = 1
    newRowList = []
    
    with open("data/{}.csv".format(stockId), "r") as csvfile:
        reader = csv.reader(csvfile)
        newRowList.append(next(reader)) # header
        
        for row in reader:
            if row[4] == '':
                continue
            
            maxList.pop(0)
            maxList.append(float(row[4])) # 最高價
            minList.pop(0)
            minList.append(float(row[5])) # 最低價
    
            try:
                rsv = round((100 * (float(row[6]) - min(minList)) / (max(maxList) - min(minList))), 2)
            except ZeroDivisionError:
                rsv = 0
                
#             if cnt <= 8:
#                 k9 = 50
#                 pass
#             elif cnt == 9: # 第九天初使 K9 值為 50
#                 k9 = 50
#             else:

            # 前 9 天的 K9 值都為 50
            if cnt >= 10:
                # 更新，發現 yahoo 的算法應該是先四捨五入後再相加
                v1 = round(rsv / 3, 2)
                v2 = round(float(k9) * 2 / 3, 2)
                k9 = round(v1+v2, 2) # 兩個都已經四捨五入，但相加還是可能會有無限小數，python 太奧妙了
                k9 = format(k9, ".2f") # 在 linux 上跑 round 會無效
                
            if len(row) >= 10:
                row[9] = rsv
            else:
                row.append(rsv)
                
            if len(row) >= 11:
                row[10] = k9
            else:
                row.append(k9)
                
            newRowList.append(row)
            cnt += 1
    
    with open("data/{}.csv".format(stockId), "w", newline="\n") as csvfile:
        writer = csv.writer(csvfile)
        for row in newRowList:
            writer.writerow(row)
            
if __name__ == "__main__":
    main()
        
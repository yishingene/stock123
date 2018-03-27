'''
計算個股 RSA, K9 值，新增至 {stockId}withRSVK9.csv

Created on 2017年11月12日
@author: Rocky
'''
import csv
import os

def main():
    for filename in os.listdir("data"):
        stockId = filename.split(".")[0]
        append(stockId)
    

def append(stockId):
    
    maxList = [0, 0, 0, 0, 0, 0, 0, 0, 0] # 9 天的最高價
    minList = [0, 0, 0, 0, 0, 0, 0, 0, 0] # 9 天的最低價
    k9 = 50
    oldK9 = None
    cnt = 1
    newRowList = []
    
    with open("data/{}.csv".format(stockId), "r") as csvfile:
        reader = csv.reader(csvfile)
        newRowList.append(next(reader)) # header
        
        for row in reader:
            if row[4] == '':
                continue
            
            i = 0
            for i in range(len(row)):
                row[i] = row[i].replace(",", "") # 把所有千分位去掉，以免影響 float 轉型
                
            maxList.pop(0)
            if row[4] == '':
                maxList.append(0.0)
            else:
                maxList.append(float(row[4])) # 最高價
                
            minList.pop(0)
            if row[5] == '':
                minList.append(0.0)
            else:
                minList.append(float(row[5])) # 最低價
    
            try:
                rsv = round((100 * (float(row[6]) - min(minList)) / (max(maxList) - min(minList))), 2)
            except ZeroDivisionError:
                rsv = 0
                
            if cnt <= 8:
                pass
            elif cnt == 9: # 第九天初使 K9 值為 50
                k9 = 50
            else:
                k9 = round((rsv / 3 + oldK9 * 2/3), 2)
                
            oldK9 = k9
            
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
#             print(row[0] + "  RSA: " + str(rsv) + "\tK9: " + str(k9))
    
    with open("data/{}.csv".format(stockId), "w", newline="\n") as csvfile:
        writer = csv.writer(csvfile)
        for row in newRowList:
            writer.writerow(row)
            
if __name__ == "__main__":
    main()
        
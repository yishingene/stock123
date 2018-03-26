'''
計算個股 RSA, K9 值，新增至 {stockId}withRSVK9.csv

Created on 2017年11月12日
@author: Rocky
'''
stockId = "0050"

import csv

maxList = [0, 0, 0, 0, 0, 0, 0, 0, 0] # 9 天的最高價
minList = [0, 0, 0, 0, 0, 0, 0, 0, 0] # 9 天的最低價
k9 = 50
oldK9 = None
cnt = 1
newRowList = []

with open("../data/{}.csv".format(stockId), "r") as csvfile:
    reader = csv.reader(csvfile)
    next(reader) # ignore header
    for row in reader:
        print(row)
        i = 0
        for i in range(len(row)):
            row[i] = row[i].replace(",", "") # 把所有千分位去掉，以免影響 float 轉型
            
        maxList.pop(0)
        maxList.append(float(row[4])) # 最高價
        minList.pop(0)
        minList.append(float(row[5])) # 最低價

        rsv = round((100 * (float(row[6]) - min(minList)) / (max(maxList) - min(minList))), 2)
        if cnt <= 8:
            pass
        elif cnt == 9: # 第九天初使 K9 值為 50
            k9 = 50
        else:
            k9 = round((rsv / 3 + oldK9 * 2/3), 2)
            
        oldK9 = k9
        
        row.append(rsv)
        row.append(k9)
        newRowList.append(row)
        cnt += 1
        print(row[0] + "  RSA: " + str(rsv) + "\tK9: " + str(k9))

with open(stockId + "withRSVK9.csv", "w", newline="\n") as csvfile:
    writer = csv.writer(csvfile)
    for row in newRowList:
        writer.writerow(row)
        
'''
計算大盤 RSA, K9 值，新增至 0000withRSVK9.csv

目前發現少數資料比如 106/09/21 的最高價，yahoo 的為 10600.34，但從證交所抓下來的為 10603.08，造成無法精準與 yahoo 的 K9 值相符

Created on 2017年11月12日
@author: Rocky
'''
import csv

def main():
    
    maxList = [0, 0, 0, 0, 0, 0, 0, 0, 0] # 9 天的最高價
    minList = [0, 0, 0, 0, 0, 0, 0, 0, 0] # 9 天的最低價
    k9 = None
    oldK9 = None
    
    newRowList = []
    cnt = 1
    with open("t00.csv", "r") as csvfile:
        reader = csv.reader(csvfile)
        newRowList.append(next(reader)) # header
        for row in reader:
            i = 0
            for i in range(len(row)):
                row[i] = row[i].replace(",", "") # 把所有千分位去掉，以免影響 float 轉型
    
    #         if row[0] == "2017/09/21":
    #             row[2] = 10600.34
            
            maxList.pop(0)
            maxList.append(float(row[2])) # 最高價
            minList.pop(0)
            minList.append(float(row[3])) # 最低價
            
            rsv = round((100 * (float(row[4]) - min(minList)) / (max(maxList) - min(minList))), 2)
            if cnt <= 8:
                k9 = 50
                pass
            elif cnt == 9: # 第九天初使 K9 值為 50
                k9 = 50
            else:
                # 更新，發現 yahoo 的算法應該是先四捨五入後再相加
                v1 = round(rsv / 3, 2)
                v2 = round(float(k9) * 2 / 3, 2)
                k9 = round(v1 + v2, 2) # 兩個都已經四捨五入，但相加還是可能會有無限小數，python 太奧妙了
                k9 = format(k9, ".2f") # 在 linux 上跑 round 會無效
                
            oldK9 = k9
            
            if len(row) == 7:
                row[5] = rsv
                row[6] = k9
            else:
                row.append(rsv)
                row.append(k9)
                
            newRowList.append(row)
            cnt += 1
    
    with open("t00.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        for row in newRowList:
            writer.writerow(row)


if __name__ == "__main__":
    main()        
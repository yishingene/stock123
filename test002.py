'''
由 test001 改，判斷 0050 成份股，排序殖利率

Created on 2018年2月28日
@author: rocky.wang
'''
import csv, datetime, time
from _collections import deque
import os, lineTool

def main():
    
    with open("0050composition.csv", "r", encoding="utf-8") as f1:
        reader = csv.reader(f1)
        msg = ""
        cond = 7
        msg += "0050成份股中平均三或五年殖利率大於{}%，一至七年平均殖利率\n".format(cond)
        for row in reader:
            stockId = row[0]
        
            li = open_file(stockId)
            
            if len(li) == 0:
                continue
            
            if li[2] > cond and li[4] > cond:
                
                if len(row[1]) == 2:
                    row[1] = row[1] + "__"
                
#                 msg += "\n%s %s  平均殖利率  三年  %.2f 五年  %.2f" %(stockId, row[1], li[2], li[4])
                msg += "\n%s %s\t%6.2f %6.2f %6.2f %6.2f %6.2f %6.2f %6.2f" %(stockId, row[1], li[0], li[1], li[2], li[3], li[4], li[5], li[6])
#                 msg += "\n%s  00.00" %(row[1])
        
        print(msg)        
    
        # 發 LINE 通知
#         lineTool.lineNotify(os.environ["LINE_TEST_TOKEN"], msg)
#         lineTool.lineNotify(os.environ["LINE_0050_TOKEN"], msg)
#         time.sleep(3)   # delays for n seconds
#         lineTool.lineNotify(os.environ["LINE_0050_TOKEN2"], msg) # 這是深似海的
#         time.sleep(3)
#         lineTool.lineNotify(os.environ["LINE_0050_TOKEN3"], msg)
#         time.sleep(3)
#         lineTool.lineNotify(os.environ["LINE_0050_TOKEN4"], msg)
#         time.sleep(3)
#         lineTool.lineNotify(os.environ["LINE_0050_TOKEN5"], msg)
#         time.sleep(3)
#         lineTool.lineNotify(os.environ["LINE_0050_TOKEN6"], msg)


def get_final_price_by_file(stockId):
    filename = "data/{}.csv".format(stockId)
    try:
        with open(filename, 'r') as f:
            lastrow = deque(csv.reader(f), 1)[0]
            return lastrow[6]
    except IndexError as e:  # empty file
        return None
    except FileNotFoundError as e:
        print(e)


def calRate(price:float, m:float, s:float):
    t = m * 1000 + s * 100 * price # 總獲利
    x = t / (price * 1000) * 100 # 總獲利 / 總成本
    return x
    #return format(x, ".2f")

def open_file(stockId):

    # i want to get final stock price by open csv file
    fname = "data/{}.csv".format(stockId)
    z = get_final_price_by_file(stockId)
#     print("%s [%s] " %(stockId, z))

    try:
        price = float(z)
    except:
        price = 100000
    
    dt = datetime.datetime.now()
    # 初使
    dict = {}
    for i in range(0, 50):
        year = dt.year - i
        dict[str(year)] = [0.0, 0.0]
        
    # TODO
    if stockId == '3711':
        return []

    with open("stockDividendSchedule/stockDividendSchedule_{}.csv".format(stockId), "r", encoding="utf-8") as f1:
        csvReader = csv.reader(f1)
        n = 1
        for row in csvReader:
            if n == 1:
                n+=1
                continue
            dict[row[1]][0] += float(row[10])
            dict[row[1]][1] += float(row[13])
    
#     dict.pop('2018')  # 一開始是因為 2018 還沒有資料，現在有了，不需要再丟棄
    cnt = 1
    m = 0.0
    s = 0.0
    li = []
    for key, value in dict.items():
        m += value[0]
        s += value[1]
        avg_m = m / float(cnt)
        avg_s = s / float(cnt)
        x = calRate(price, avg_m, avg_s)
        li.append(x)
#         print("%s year %s" %(cnt, x))
        cnt += 1
        pass
    
    return li


if __name__ == '__main__':
    
    main()
    

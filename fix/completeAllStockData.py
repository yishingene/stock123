'''
之前的資料到 201802 月份，補上三月份

Created on 2018年3月26日
@author: rocky.wang
'''
import os, csv
from twse_crawler import TWSECrawler
import time

def main():

    for filename in os.listdir("../data"):
        processFile(filename)
        time.sleep(5)

#     processFile("9958.csv")
        
def processFile(filename):    
    
    stockId = filename.split(".")[0]
        
    rowDict = {}
    # 讀舊資料轉換格式
    with open("../data/"+filename) as f1:
        for row in csv.reader(f1):
            row[0] = row[0].strip()
            row[0] = '/'.join([str(int(row[0].split('/')[0]) + 1911)] + row[0].split('/')[1:])
            
            row[1] = int(row[1].replace(',', ''))
            row[2] = int(row[2].replace(',', ''))
            
            # 3~6
            for i in range(3, 7):
                if row[i].replace(',', '') == '--' or row[i] == '':
                    row[i] = None
                else:
                    row[i] = float(row[i].replace(',', ''))
            
            row[7] = row[7].strip()
            row[8] = int(row[8].replace(',', ''))

            rowDict[row[0]] = row
            
    # 撈取三月份新資料
    twseCrwaler = TWSECrawler()
    rowList = twseCrwaler.fetch2(2018, 3, stockId)
    for row in rowList:
        rowDict[row[0]] = row
        
    with open("../data/"+filename, "w", newline="") as f1:
        writer = csv.writer(f1)
        writer.writerow(['日期', '成交股數', '成交金額', '開盤價', '最高價', '最低價', '收盤價', '漲跌價差', '成交筆數', 'RSV', 'K9'])
        for row in rowDict.values():
            writer.writerow(row)
            

#     with open("../data/"+filename, "w", newline="") as f1:
#         writer = csv.writer(f1)
#         writer.writerow(['日期', '成交股數', '成交金額', '開盤價', '最高價', '最低價', '收盤價', '漲跌價差', '成交筆數', 'RSV', 'K9'])
#         for row in rowDict.values():
#             for row in rowList:
#                 writer.writerow(row)
    
if __name__ == "__main__":
    main()

    
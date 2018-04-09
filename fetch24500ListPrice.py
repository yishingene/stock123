'''
Created on 2018年4月9日
@author: rocky.wang
'''
from googleService import GooglesheetService
import csv

googlesheetService = GooglesheetService("1AaYDVOacDO60MgPTf0Taf4k-ZGIupL9bJM7ovMTIAhM")

cnt = 0
for value in googlesheetService.getValues("工作表1"):
    cnt += 1

    try:
        with open("data/{}.csv".format(value[1]), encoding="MS950") as f1:
            row = list(csv.reader(f1))[-1]
            if float(row[6]) < float(value[0]):
                
                diff = float(value[0]) - float(row[6])
                pect = round(diff / float(row[6]) * 100, 2)
                
                if pect > 30:
                    print("{} {}\t目標價: {}\t現價: {}\t({}%)".format(value[1], value[2], value[0], row[6], pect))
            else:
#                 print(value)
                pass
    except:
#         print(value[1], "no file")
        pass

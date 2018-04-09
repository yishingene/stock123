'''
Created on 2018年4月9日
@author: rocky.wang
'''
from googleService import GooglesheetService

googlesheetService = GooglesheetService("1AaYDVOacDO60MgPTf0Taf4k-ZGIupL9bJM7ovMTIAhM")

cnt = 0
for v in googlesheetService.getValues("工作表1"):
    print(v)
    cnt += 1
    
print(cnt)    

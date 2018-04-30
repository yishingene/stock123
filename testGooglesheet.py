'''
Created on 2018年4月30日
@author: Eit
'''
from googleService import GooglesheetService
import time

gid = "1v_h_IGT9gRYqm1jIf4N413k1KqwGRKwxYx0_ww5Tnz0"
rangeName = "工作表1" # ensure you have a sheet named it

googlesheetService = GooglesheetService(gid) # init service by spreadsheetId

while True:
    
    rowList = googlesheetService.getValues(rangeName)
    for row in rowList:
        print(row)
        
    time.sleep(3)
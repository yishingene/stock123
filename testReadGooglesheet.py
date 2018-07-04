'''

Created on 2018年6月14日
@author: rocky.wang
'''
from googleService import GooglesheetService

gid = "1F3cT6ltHQ7gOYxCPSrPJGvMpUt3b5mRJIMR0gJ5ITr8"
rangeName = "掃描清單"

googlesheetService = GooglesheetService(gid) # init service by spreadsheetId

rowList = googlesheetService.getValues(rangeName)
rowNum = 0
for row in rowList:
    rowNum += 1
    if rowNum == 1:
        continue
    
    name = row[0]
    url = row[1].replace("https://docs.google.com/spreadsheets/d/", "").split("/")[0]
    token = row[2]
    print(name, url, token)
        

'''
Created on 2018年3月23日
@author: rocky.wang
'''
from googleService import GooglesheetService


googlesheetService = GooglesheetService("1033HVmaLyxYkfiX889L5J4ypBuw9xvowotKGPtXWRV0")

googlesheetService.clearSheet("00676R")

for i in range(1, 3001):
    rowList = [[i+1, i+2, i+3], [4, 5, 6], [4, 5, 6], [4, 5, 6], [4, 5, 6], [4, 5, 6], [4, 5, 6], [4, 5, 6], [4, 5, 6], [4, 5, 6], [4, 5, 6], [4, 5, 6], [4, 5, 6], [4, 100, 5, 6, 7, 8, 9 , 1], [1], [2], [3]]
    googlesheetService.appendSheet("00676R", rowList)


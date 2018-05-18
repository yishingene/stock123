'''

Created on 2018年5月9日
@author: rocky.wang
'''
import csv


def main():

    stockId = "1215"

    diffRate = calDiff(stockId)
    print(diffRate)    


def calDiff(stockId):

    with open("data/{}.csv".format(stockId)) as f1:
        rowList = list(csv.reader(f1))[-30:]
    
    maxPrice = 0
    minPrice = 100000
    for row in rowList:
        price = float(row[6])
        if price > maxPrice:
            maxPrice = price
        if price < minPrice:
            minPrice = price
    
    diffRate = round((maxPrice - minPrice) / minPrice, 4)
    return diffRate


if __name__ == "__main__":
    main()
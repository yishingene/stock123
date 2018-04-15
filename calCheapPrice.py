'''
Created on 2018年4月15日
@author: Rocky
'''
import csv
import os

def main():
    
    for filename in os.listdir("data"):
        sid = filename.split(".")[0]
        process(sid)
    
    pass

def process(stockId):
    with open("data/{}.csv".format(stockId)) as f1:
        rows = list(csv.reader(f1))[-250:]
        
        highPrice = 0
        lastPrice = 0
        for row in rows:
            
            zPrice = None
            if not row[6] == '收盤價':
                zPrice = float(row[6])
            else:
                continue
            
            lastPrice = zPrice
            if zPrice > highPrice:
                highPrice = zPrice
                
        diffPrice = highPrice - lastPrice
        if diffPrice > 0:
            
            diffPct = round(lastPrice / highPrice, 2)
            
            if diffPct < 0.6:
                print("{}\t{}  {}\t{}".format(stockId, highPrice, lastPrice, diffPct))
        
        
    pass

if __name__ == "__main__":
    main()


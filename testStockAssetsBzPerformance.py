'''
抓取稅後淨利 & 長期負債做計算

testStockAssetsStatus.py & testStockBzPerformance.py 的統整

Created on 2018年4月8日
@author: rocky.wang
'''
from testStockAssetsStatus import fetchStockAssetsStatus
from testStockBzPerformance import fetchStockBzPerformance

stockId = "1264"
stockId = "1215"
stockId = "2002"

longTermDebit = fetchStockAssetsStatus(stockId)
pureEarn = fetchStockBzPerformance(stockId)

rate = round(longTermDebit / pureEarn, 2)

print(longTermDebit, pureEarn, rate)



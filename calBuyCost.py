'''
我只是想要自動算出買賣成本

Created on 2018年4月8日
@author: rocky.wang
'''
stockNum = 1000

buyPrice = 20
salePrice = 20.25

buyPrice = 8.75
salePrice = 8.71

buyPrice = 49.30
salePrice = 49.60

buyCost = stockNum * buyPrice * 0.001425
print("buy cost:\t{:.2f}".format(buyCost))

saleCost1 = stockNum * salePrice * 0.001425
saleCost2 = stockNum * salePrice * 0.003

print("sale cost1:\t{:.2f}".format(saleCost1))
print("sale cost2:\t{:.2f}".format(saleCost2))
totalCost = buyCost + saleCost1 + saleCost2
print("total cost:\t{:.2f}".format(totalCost))

print("-----------------------")

buyMoney = buyPrice * stockNum
saleMoney = salePrice * stockNum
print("buy money:\t{:.2f}".format(buyMoney))
print("sale money:\t{:.2f}".format(saleMoney))
print("-----------------------")
print("win money:\t{:.2f}".format(saleMoney-buyMoney-totalCost))




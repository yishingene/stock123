'''
Created on 2018年3月27日
@author: Eit
'''
import csv

with open("data/00703.csv", "r") as f1:
    reader = csv.reader(f1)
    next(reader)
    
    for row in reader:
        print(row)
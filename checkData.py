'''
Created on 2018年3月26日
@author: Rocky
'''
import os
import csv


for filename in os.listdir("data"):
    with open("data/" + filename) as f1:
        reader = csv.reader(f1)
        line = next(reader)
        if line[0] == '日期':
            print("OK")
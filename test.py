'''
Created on 2018年3月29日
@author: rocky.wang
'''
import requests

url = "https://histock.tw/stock/financial.aspx?no=1215&st=2"

resp = requests.get(url)
print(resp.text)
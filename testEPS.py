'''
Created on 2018年4月8日
@author: rocky.wang
'''

import requests

url = "http://mops.twse.com.tw/mops/web/ajax_t163sb19"

data = {"TYPEK": "sii", "code": "02", "year": "106", "season": "02", "firstin": "1", "step": "1" }

resp = requests.post(url, data=data, headers={"User-Agent" : "Chrome/31.0.1650.63"})

resp.encoding="utf-8"
print(resp.text)

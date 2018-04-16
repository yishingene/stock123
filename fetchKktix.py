'''
抓取 kktix，若有新活動通知

Created on 2018年4月8日
@author: rocky.wang
'''
import requests

from bs4 import BeautifulSoup
import csv
import lineTool
import os

# url = "http://mops.twse.com.tw/mops/web/ajax_t163sb19"
# data = {"TYPEK": "sii", "code": "02", "year": "106", "season": "02", "firstin": "1", "step": "1" }
# resp = requests.post(url, data=data, headers={"User-Agent" : "Chrome/31.0.1650.63"})

url = "https://kktix.com/events"
resp = requests.get(url)

soup = BeautifulSoup(resp.text, "lxml")

liList = soup.find("ul", {"class": "event-list"}).findAll("li", {"class": "clearfix"})

kktixList = []
with open("kktix.txt", encoding="utf-8") as f1:
    kktixList = list(csv.reader(f1))

with open("kktix.txt", "a", newline="", encoding="utf-8") as f1:
    writer = csv.writer(f1)
    
    messageList = []
    for li in liList:
        title = li.find("h2").find("a").text
        
        description = li.find("div", {"class": "description"}).text
        
        href = li.find("h2").find("a").get("href")
        
        message = title + "\n\n" + description + "\n" + href
        
        if not [href] in kktixList:
            writer.writerow([href])
            messageList.append(message)
    
    if len(messageList) > 0:
        notifyMessage = ""
        for msg in messageList:
            notifyMessage += msg + "\n----------------------------------------\n\n"
        lineTool.lineNotify(os.environ["LINE_TEST_TOKEN"], notifyMessage)
            
            

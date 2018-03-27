import requests, time
import datetime
import csv
import os
from matplotlib.mlab import csv2rec


class TWSECrawler():
    
    def __init__(self):
        pass
    
    def _make_datatuple(self, data):
        """Convert '106/05/01' to '2017/05/01'"""
        data[0] = data[0].strip()
        if not data[0].startswith("20"):
            data[0] = '/'.join([str(int(data[0].split('/')[0]) + 1911)] + data[0].split('/')[1:])
        
        data[1] = int(data[1].replace(',', ''))
        data[2] = int(data[2].replace(',', ''))
        
        # 3~6
        for i in range(3, 7):
            if data[i].replace(',', '') == '--':
                data[i] = None
            else:
                data[i] = float(data[i].replace(',', ''))
        
        data[7] = data[7].strip()
        data[7] = float(data[7])
        data[8] = int(data[8].replace(',', ''))
        return data

    def purify(self, data):
        return [self._make_datatuple(d) for d in data]

    
    ''' 抓取個股歷史資料 '''
    def fetchMonthData(self, year, month, stockId, retry=2):

        ym = '%d%02d' %(year, month)

        print('TWSE Fetching Stock [%s], ym: [%s]' %(stockId, ym), flush=True)        
        
        url = "http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date=" + ym + "01&stockNo=" + stockId
        print(url, flush=True)
        stat = None
        try:
            r = requests.get(url)
            data = r.json()
            print(data, flush=True)
            
            stat = data['stat']
            
            if data['stat'] == 'OK':
                return self.purify(data['data'])
            else:
                # 目前不應該有查不到資料的問題
                raise Exception("stat error")
        except Exception as e:
            print(e, flush=True)
            if retry > 0:
                print("retry %s times, stat: %s" %(retry, stat), flush=True)
                if stat == '很抱歉，沒有符合條件的資料!' or stat == '查詢日期小於81年1月4日，請重新查詢!':
                    time.sleep(5)
                else:
                    time.sleep(60)
                    
                return self.fetch(ym, stockId, retry-1)
            else:
                if stat != '很抱歉，沒有符合條件的資料!':
                    raise e
                else:
                    return None


    def fetchStockInfo(self, stockId):
        s = requests.Session()
        s.get("http://mis.twse.com.tw/stock/index.jsp")
        url = "http://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=tse_{stockId}.tw&_={time}".format(stockId=stockId, time=int(time.time()) * 1000)
        r = s.get(url)
        print("\nGET {}\n{}".format(url, r.text))
        return r.json()

    def fetchAllStockData(self):
        
        pass
    
    
    def fetchAllStockFinalData(self, dt=datetime.datetime.now()):
        
        url = "http://www.twse.com.tw/exchangeReport/MI_INDEX?response=json&date=%s&type=ALLBUT0999&_=%s" %(dt.strftime("%Y%m%d"), int(time.time()*1000))
        r = requests.get(url)
        print("GET %s\nResponse => %s" %(url, r.json()))
        
        js = r.json()
        if js.get("stat") != "OK":
            print("%s 查無資料" %(dt.strftime("%Y%m%d")))
            return
            
        for data in js.get("data5"):
            sign = '-' if data[9].find('green') > 0 else ''
            date = "{}/{}/{}".format(js["date"][0:4], js["date"][4:6], js["date"][6:8])
            row = [date, data[2], data[4], data[5], data[6], data[7], data[8], sign+data[10], data[3]]
            row = self._make_datatuple(row)
            
            stockId = data[0]
            
            if not os.path.exists("data/{}.csv".format(stockId)):
#                 with open("data/{}.csv".format(stockId), "a", newline="") as f1:    
#                     writer = csv.writer(f1)
#                     writer.writerow(["日期","成交股數","成交金額","開盤價","最高價","最低價","收盤價","漲跌價差","成交筆數","RSV","K9"])
                # 先略過，不處理，之後再處理這些新的
                continue
            
            # 先讀出舊的資料
            rowDict = {}
            with open("data/{}.csv".format(stockId), "r") as f1:
                for row1 in csv.reader(f1):
                    rowDict[row1[0]] = row1
            
            rowDict[row[0]] = row
                      
            with open("data/{}.csv".format(stockId), "w", newline="") as f1:
                writer = csv.writer(f1)
                for d in rowDict.values():
                    writer.writerow(d)


if __name__ == "__main__":
#     dt = datetime.datetime(2018, 3, 26)
    cr = TWSECrawler()
    cr.fetchAllStockFinalData()
    
    
    
import requests, time
import datetime
import csv
import os


class TWSECrawler():
    
    def __init__(self):
        pass
    
    def _make_datatuple(self, data):
        """Convert '106/05/01' to '2017/05/01'"""
        data[0] = data[0].strip()
        if not data[0].startswith("20") and not data[0].startswith("19"):
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

    ''' 單純想爬最新資料 '''
    def crawlStockInfo(self, stockId):
        s = requests.Session()
        s.get("http://mis.twse.com.tw/stock/index.jsp")
        url = "http://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=tse_{stockId}.tw&_={time}".format(stockId=stockId, time=int(time.time()) * 1000)
        r = s.get(url)
        print("GET URL => {}\nResponse => {}".format(url, r.text.strip().replace("False", "false")))
        return r.json()
        

    ''' 爬最新資料並寫回 csv 檔案 '''
    def fetchStockInfo(self, stockId):

        # 讀舊資料出來
        rowDict = {}
        with open("data/{}.csv".format(stockId), encoding="MS950") as f1:
            for row in csv.reader(f1):
                rowDict[row[0]] = row
        
        js = self.crawlStockInfo(stockId)
        # 先不考慮錯的時候，直接讓它丟出，最外面直接 line notify 錯誤
#         if js["rtcode"] == "0000":
        v = int(js["msgArray"][0]["v"]) # 成交股數
        z = float(js["msgArray"][0]["z"]) # 現價
        y = float(js["msgArray"][0]["y"]) # 昨日價
        
        dt = "{}/{}/{}".format(js["msgArray"][0]["d"][0:4], js["msgArray"][0]["d"][4:6], js["msgArray"][0]["d"][6:8])
        
        row = [dt, v, int(v*z), js["msgArray"][0]["o"], js["msgArray"][0]["h"], js["msgArray"][0]["l"], js["msgArray"][0]["z"], round(z-y, 2), "", "", ""]
        rowDict[row[0]] = row
                
        with open("data/{}.csv".format(stockId), "w", newline="", encoding="MS950") as f1:
            writer = csv.writer(f1)
            for d in rowDict.values():
                writer.writerow(d)
                
        self.appendData(stockId)


    ''' 收盤後，爬所有收盤股票資料 '''    
    def fetchAllStockFinalData(self, dt=datetime.datetime.now()):
        
        url = "http://www.twse.com.tw/exchangeReport/MI_INDEX?response=json&date=%s&type=ALLBUT0999&_=%s" %(dt.strftime("%Y%m%d"), int(time.time()*1000))
        r = requests.get(url)
        print("GET %s\nResponse => %s" %(url, r.json()))
        
        js = r.json()
        if js.get("stat") != "OK":
            print("%s 查無資料" %(dt.strftime("%Y%m%d")))
            return
            
        for data in js.get("data5"):
            
            stockId = data[0]
            
            if data[9].find('red') > 0:
                sign = '+'
            else:
                sign = '-' if data[9].find('green') > 0 else ''
                
            date = "{}/{}/{}".format(js["date"][0:4], js["date"][4:6], js["date"][6:8])
            row = [date, data[2], data[4], data[5], data[6], data[7], data[8], sign+data[10], data[3], "", ""] # 後面兩個空值是 RSV & K9
            row = self._make_datatuple(row)
            if not os.path.exists("data/{}.csv".format(stockId)):
#                 with open("data/{}.csv".format(stockId), "a", newline="") as f1:    
#                     writer = csv.writer(f1)
#                     writer.writerow(["日期","成交股數","成交金額","開盤價","最高價","最低價","收盤價","漲跌價差","成交筆數","RSV","K9"])
                # 先略過，不處理，之後再處理這些新的
                continue
            
            # 讀出舊的資料
            rowDict = {}
            with open("data/{}.csv".format(stockId), "r", encoding="MS950") as f1:
                for row1 in csv.reader(f1):
                    rowDict[row1[0]] = row1
            
            rowDict[row[0]] = row
                      
            with open("data/{}.csv".format(stockId), "w", newline="", encoding="MS950") as f1:
                writer = csv.writer(f1)
                for d in rowDict.values():
                    writer.writerow(d)
            
            # 更新 RSV & K9
            self.appendData(stockId)


    ''' append RSV & K9 data '''
    def appendData(self, stockId):
        
        print("Process append RSV & K9 data for {}".format(stockId))
        
        maxList = [0, 0, 0, 0, 0, 0, 0, 0, 0] # 9 天的最高價
        minList = [0, 0, 0, 0, 0, 0, 0, 0, 0] # 9 天的最低價
        k9 = 50
        cnt = 1
        newRowList = []
        
        with open("data/{}.csv".format(stockId), "r", encoding="MS950") as csvfile:
            reader = csv.reader(csvfile)
            newRowList.append(next(reader)) # header
            for row in reader:
                if row[4] == '':
                    continue
                
                maxList.pop(0)
                maxList.append(float(row[4])) # 最高價
                minList.pop(0)
                minList.append(float(row[5])) # 最低價
        
                try:
                    rsv = round((100 * (float(row[6]) - min(minList)) / (max(maxList) - min(minList))), 2)
                except ZeroDivisionError:
                    rsv = 0
                    
                # 前 9 天的 K9 值都為 50
                if cnt >= 10:
                    # 更新，發現 yahoo 的算法應該是先四捨五入後再相加
                    v1 = round(rsv / 3, 2)
                    v2 = round(float(k9) * 2 / 3, 2)
                    k9 = round(v1+v2, 2) # 兩個都已經四捨五入，但相加還是可能會有無限小數，python 太奧妙了
                    k9 = format(k9, ".2f") # 在 linux 上跑 round 會無效
                    
                if len(row) >= 10:
                    row[9] = rsv
                else:
                    row.append(rsv)
                    
                if len(row) >= 11:
                    row[10] = k9
                else:
                    row.append(k9)
                    
                newRowList.append(row)
                cnt += 1
        
        with open("data/{}.csv".format(stockId), "w", newline="\n", encoding="MS950") as csvfile:
            writer = csv.writer(csvfile)
            for row in newRowList:
                writer.writerow(row)


if __name__ == "__main__":

    dt = datetime.datetime.now()
    # 若要指定日期
#     dt = datetime.datetime(2018, 3, 27)
        
    cr = TWSECrawler()
    
#     cr.fetchAllStockFinalData(dt)
    
    js = cr.fetchStockInfo("0056")
    
    
    
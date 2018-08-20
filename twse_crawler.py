import requests, time
import datetime
import csv
import os
import lineTool


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
        
#         url = "http://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=otc_{stockId}.tw&_={time}".format(stockId=stockId, time=int(time.time()) * 1000)
        r = s.get(url)
        print("GET URL => {}\n{}".format(url, r.text.strip().replace("False", "false")))
        return r.json()
    
    
    def crawlStockInfoOtc(self, stockId):
        s = requests.Session()
        s.get("http://mis.twse.com.tw/stock/index.jsp")
        url = "http://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=otc_{stockId}.tw&_={time}".format(stockId=stockId, time=int(time.time()) * 1000)
        r = s.get(url)
        print("GET URL => {}\n{}".format(url, r.text.strip().replace("False", "false")), flush=True)
        return r.json()    
        

    ''' 爬最新資料並寫回 csv 檔案 '''
    def fetchStockInfo(self, stockId):

        js = self.crawlStockInfo(stockId)

        # {"userDelay":500,"rtmessage":"   ","rtcode":"0000"}
        if js["rtcode"] == "0000" and js["rtmessage"] != "OK":
            print("response 0000 but rtmessage:[{}], sleep and try again...".format(js["rtmessage"]))
            time.sleep(5)
            js = self.crawlStockInfo(stockId)
            print(js)
        
        if js["rtcode"] == "0000" and js["rtmessage"] != "OK":
            print("response 0000 but rtmessage:[{}], sleep and try again...".format(js["rtmessage"]))
            time.sleep(5)
            js = self.crawlStockInfo(stockId)
            print(js)

        # 不知道為什麼，有些就是會暫時沒資料
        if js["rtcode"] == "0000" and js["rtmessage"] == "OK" and len(js["msgArray"]) == 0:
            lineTool.lineNotify(os.environ["LINE_TEST_TOKEN"], "{} 查詢成功卻無資料".format(stockId))
            print("查詢成功卻無資料")
            return
        
        if js["rtcode"] == "0000" and js["rtmessage"] == "OK" and js["msgArray"][0].get("o", "") == '':
            lineTool.lineNotify(os.environ["LINE_TEST_TOKEN"], "{} 查詢成功卻無資料".format(stockId))
            print("查詢成功卻無開盤價格")
            return
        
        if not js["msgArray"][0]["d"] == datetime.datetime.now().strftime('%Y%m%d'):
            print("查無今日資料不繼續處理檔案")
            return
        

        # 讀舊資料出來
        rowDict = {}
        with open("data/{}.csv".format(stockId), encoding="MS950") as f1:
            for row in csv.reader(f1):
                rowDict[row[0]] = row
        
        # 先不考慮錯的時候，直接讓它丟出，最外面直接 line notify 錯誤
#         if js["rtcode"] == "0000":
        
        o = round(float(js["msgArray"][0]["o"]), 2)
        h = round(float(js["msgArray"][0]["h"]), 2)
        l = round(float(js["msgArray"][0]["l"]), 2)
        z = round(float(js["msgArray"][0]["z"]), 2) # 現價
        y = round(float(js["msgArray"][0]["y"]), 2) # 昨日價
        v = int(js["msgArray"][0]["v"]) * 1000 # 成交股數 (v 在這邊應該是張數，要自己 * 1000 才會變真實的股數)
        
        dt = "{}/{}/{}".format(js["msgArray"][0]["d"][0:4], js["msgArray"][0]["d"][4:6], js["msgArray"][0]["d"][6:8])
        diff = "+" + format(round(z-y, 2), ".2f") if z-y > 0 else format(round(z-y, 2), ".2f")
        row = [dt, v, int(v*z), format(o, ".2f"), format(h, ".2f"), format(l, ".2f"), format(z, ".2f"), diff, "", "", ""]
        rowDict[row[0]] = row
                
        self.appendDataByRowList(stockId, rowDict)
        

    ''' 收盤後，爬所有收盤股票資料 '''    
    def fetchAllStockFinalData(self, dt=datetime.datetime.now()):
        
        url = "http://www.twse.com.tw/exchangeReport/MI_INDEX?response=json&date=%s&type=ALLBUT0999&_=%s" %(dt.strftime("%Y%m%d"), int(time.time()*1000))
        r = requests.get(url)
        print("GET %s\nResponse => %s" %(url, r.json()))
        
        js = r.json()
        if js.get("stat") != "OK":
            print("%s 查無資料" %(dt.strftime("%Y%m%d")))
            return
        
        # 因為有 K 值要處理，不能只抓存單一值，必須從頭開始存起，改通知我自己，有新的代號要處理歷史資料
        newStockIdList = []    
        
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
                newStockIdList.append(stockId)
                continue
            
            # 讀出舊的資料
            rowDict = {}
            with open("data/{}.csv".format(stockId), "r", encoding="MS950") as f1:
                for row1 in csv.reader(f1):
                    rowDict[row1[0]] = row1
            
            if row[3] != None:
                row[3] = format(round(row[3], 2), ".2f")
            if row[4] != None:
                row[4] = format(round(row[4], 2), ".2f")
            if row[5] != None:
                row[5] = format(round(row[5], 2), ".2f")
            if row[6] != None:
                row[6] = format(round(row[6], 2), ".2f")
            
            rowDict[row[0]] = row
                      
            self.appendDataByRowList(stockId, rowDict)
                      
        lineTool.lineNotify(os.environ["LINE_TEST_TOKEN"], newStockIdList)
        
#             with open("data/{}.csv".format(stockId), "w", newline="", encoding="MS950") as f1:
#                 writer = csv.writer(f1)
#                 for d in rowDict.values():
#                     writer.writerow(d)
#             
#             # 更新 RSV & K9
#             self.appendData(stockId)


    ''' append RSV & K9 data，不再開檔，讓效率好一點 '''
    def appendDataByRowList(self, stockId, rowDict):
        
        print("Process append RSV & K9 data for new {}".format(stockId), flush=True)
        
        maxList = [0, 0, 0, 0, 0, 0, 0, 0, 0] # 9 天的最高價
        minList = [0, 0, 0, 0, 0, 0, 0, 0, 0] # 9 天的最低價
        k9 = 50
        cnt = 1
        newRowList = []
        
        idx = 0
        for row in rowDict.values():
            if idx == 0:
                newRowList.append(row) # header
                idx += 1
                continue
            
            if row[4] == '' or row[4] == None:
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
                
            row[9] = format(rsv, ".2f")
            row[10] = k9
                
            newRowList.append(row)
            cnt += 1
        
        with open("data/{}.csv".format(stockId), "w", newline="\n", encoding="MS950") as csvfile:
            writer = csv.writer(csvfile)
            for row in newRowList:
                writer.writerow(row)


    '''
    OTC 是一開始沒有想到的，那時太菜了，還不知道有分上市上櫃，目前的需求只是把每日收盤價格存下來後，可以供查詢就好，所以就不比照之前的處理方式了 
    '''
    def fetchOtcDailyCloseQuotes(self):
    
        now = datetime.datetime.now()
        dt = str(int(now.strftime('%Y')) - 1911) + now.strftime('/%m/%d') # format example => 107/07/13 
        url = "http://www.tpex.org.tw/web/stock/aftertrading/daily_close_quotes/stk_quote_result.php?l=zh-tw&d={}&_={}".format(dt, int(time.time() * 1000))
        print(url)
    
        r = requests.get(url)
        js = r.json()
        print(js)
        
        dt = now.strftime('%Y/%m/%d')
        rowList = []
        for data in js["aaData"]:
            rowList.append(data)
            # 日期,成交股數,成交金額,開盤價,最高價,最低價,收盤價,漲跌價差,成交筆數,RSV,K9
            row = [dt, data[8], data[9], data[4], data[5], data[6], data[2]]
    
        with open("data_daily_close_quotes/otc_{}.csv".format(now.strftime('%Y%m%d')), "w", encoding="utf-8", newline="") as f1:
            csv.writer(f1).writerows(rowList)



if __name__ == "__main__":

    # 若要指定日期
#     dt = datetime.datetime.now()
#     dt = datetime.datetime(2018, 3, 27)
        
#     cr = TWSECrawler()
#     cr.fetchAllStockFinalData(dt)

    # 測試上櫃即時資料
#     cr = TWSECrawler()    
#     #js = cr.crawlStockInfoOtc("6803")
#     js = cr.crawlStockInfoOtc("5512")
#      
#     name = js["msgArray"][0]["n"]
#     openPrice = js["msgArray"][0]["o"]
#     nowPrice = js["msgArray"][0]["z"]
#     volume = js["msgArray"][0]["v"]
#     print(name, openPrice, nowPrice, volume)
    
    # 測試上市即時資料
#     cr = TWSECrawler()    
#     js = cr.crawlStockInfo("t00")
    
    # 測試上櫃收盤資料
    cr = TWSECrawler()    
    cr.fetchOtcDailyCloseQuotes()
    
    
    
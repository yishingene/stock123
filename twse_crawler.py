import requests, collections, time

DATATUPLE = collections.namedtuple('Data', ['date', 'capacity', 'turnover', 'open', 'high', 'low', 'close', 'change', 'transaction'])
    
TWSE_BASE_STOCK_URL = "http://www.twse.com.tw/exchangeReport/STOCK_DAY"

class TWSECrawler():
    
    def __init__(self):
        pass
    
    def _make_datatuple(self, data):
        """Convert '106/05/01' to '2017/05/01'"""
        data[0] = data[0].strip()
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

    
    def fetch(self, ym, sid, retry = 2):

        print('TWSE Fetching Stock [%s], ym: [%s]' %(sid, ym), flush=True)        
        
        url = TWSE_BASE_STOCK_URL + "?response=json&date=" + ym + "01&stockNo=" + sid
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
                    
                return self.fetch(ym, sid, retry - 1)
            else:
                if stat != '很抱歉，沒有符合條件的資料!':
                    raise e
                else:
                    return None


    def fetch2(self, year: int, month: int, sid: str, retry = 2):
        ym = '%d%02d' %(year, month)
        return self.fetch(ym, sid, retry)
            

'''
service help you to easy create, modify, delete, get googlesheet

Created on 2018年3月18日
@author: rocky.wang
'''
from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import time
import ssl
import traceback
from googleapiclient.errors import HttpError

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'


class GooglesheetService():
    
    service = None
    spreadsheetId = None
    
    requestCnt = 0
    requestTime = time.time()

    def checkQuota(self):

        self.requestCnt += 1
        now = time.time()
        
        if now - self.requestTime > 60 and self.requestCnt > 90:
            print("額度快要超過上限睡上 65 秒後再繼續...")
            time.sleep(65) # 避免只睡一分鐘有風險
            self.requestCnt = 1
            self.requestTime = time.time()
    
    
    def __init__(self, spreadsheetId):
        self.spreadsheetId = spreadsheetId
        # init service
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?version=v4')
        
        try:
            self.service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)
        except ssl.SSLEOFError as e:
            print("ssl.SSLEOFError occur, try again")
            time.sleep(5)
            self.service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)

        
    def get_credentials(self):
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir, 'sheets.googleapis.com-python-quickstart.json')
    
        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else: 
                # Needed only for compatibility with Python 2.6
    #             credentials = tools.run(flow, store)
                print("pass")
            print('Storing credentials to ' + credential_path)
        return credentials


    ''' add a new sheet and return sheetId '''
    def addSheet(self, title):
        self.checkQuota()
        body = {
          "requests": [
                {
                    "addSheet": {
                        "properties": {
                            "title": title,
                            "gridProperties": {
                                "rowCount": 20,
                                "columnCount": 10
                            },
                        }
                    }
                }
            ]
        }
        request = self.service.spreadsheets().batchUpdate(spreadsheetId=self.spreadsheetId, body=body)
        response = request.execute()
        return response["replies"][0]["addSheet"]["properties"]["sheetId"]

    def deleteSheet(self, sheetId):
        self.checkQuota()
        
        body = {
            "requests": [
                {
                  "deleteSheet": {
                    "sheetId": sheetId
                  }
                }
            ]
        }
        request = self.service.spreadsheets().batchUpdate(spreadsheetId=self.spreadsheetId, body=body)
        response = request.execute()
        print(response)
        
    
    def deleteSheetByRangeName(self, rangeName):
        self.checkQuota()
        
        sheetId = self.getSheetIdByRangeName(rangeName)
        
        if sheetId != None:
            self.deleteSheet(sheetId)
        
    
    def updateSheet(self, rangeName, rowList):
        self.checkQuota()
        
        body = {
            "values" : rowList
        }
        result = self.service.spreadsheets().values().update(spreadsheetId=self.spreadsheetId, range=rangeName, valueInputOption="USER_ENTERED", body=body).execute()
#         print('{0} cells updated.'.format(result.get('updatedCells')));
#         print("%s" %(json.dumps(result, indent=4)))

    def appendSheet(self, rangeName, rowList):
        self.checkQuota()
        
        body = {
            "values" : rowList
        }
        result = self.service.spreadsheets().values().append(spreadsheetId=self.spreadsheetId, range=rangeName, valueInputOption="RAW", body=body).execute()
#         print('{0} cells updated.'.format(result.get('updatedCells')));
#         print("%s" %(json.dumps(result, indent=4)))
    
    
    def clearSheet(self, rangeName):
        self.checkQuota()
        self.service.spreadsheets().values().clear(spreadsheetId=self.spreadsheetId, range=rangeName, body={}).execute()
    
    
    def getValues(self, rangeName):
        self.checkQuota()
        try:
            result = self.service.spreadsheets().values().get(spreadsheetId=self.spreadsheetId, range=rangeName).execute()
#         except HttpError as e:
        except:
            print("cannot read spreadsheet values, sleep and try again")
            traceback.print_exc()
            time.sleep(180)
            result = self.service.spreadsheets().values().get(spreadsheetId=self.spreadsheetId, range=rangeName).execute()
            
        return result.get('values', [])
    
    
    rangeDataResp = None
    
    def getRangeData(self, includeGridData=False):
        self.checkQuota()
        ranges = [] # empty list means get all ranges data
        request = self.service.spreadsheets().get(spreadsheetId=self.spreadsheetId, ranges=ranges, includeGridData=includeGridData)
        
        self.rangeDataResp = request.execute()
        return self.rangeDataResp
    
    
    def getRangeNameList(self):

        if self.rangeDataResp == None:
            self.getRangeData()
            
        return [sheet["properties"]["title"] for sheet in self.rangeDataResp["sheets"] if sheet["properties"]["title"] != None]

    # issue，必定先呼叫 getRangeNameList 才能拿到最新的資料，但我目前不想每次都重新呼叫
    def getSheetIdByRangeName(self, rangeName):
        self.checkQuota()
        
        for sheet in self.rangeDataResp["sheets"]:
            if sheet["properties"]["title"] == rangeName:
                return sheet["properties"]["sheetId"] 
            
        return None
    
    # TODO get all sheet datas
    
    
    
if __name__ == "__main__":
    pass
    
    
    


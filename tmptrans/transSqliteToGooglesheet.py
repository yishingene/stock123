'''
sqlite to googlesheet

Created on 2018年3月22日
@author: rocky.wang
'''
import os
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from googleService import GooglesheetService

ph = os.path.dirname(os.path.abspath(__file__))
sqname = "sqlite:///" + os.path.join(ph, "stock.sqlite")

Base = declarative_base()
engine = create_engine(sqname, echo=False)

class StockPrice(Base):
    
    __tablename__ = 'STOCK_PRICE'
    
    id = Column(Integer, primary_key=True)
    stockId = Column(String) # 股票代號
    txDate = Column(String) # 交易日期
    txCount = Column(Integer) # 成交筆數
    txAmount = Column(Integer) # 成交股數
    txMoney = Column(Integer) # 成交金額
    openPrice = Column(Float)
    highPrice = Column(Float)
    lowPrice = Column(Float)
    closePrice = Column(Float)
    diffPrice = Column(String) # 漲跌價差
    
    def __repr__(self):
        return "StockPrice => {}, {}, {}, {}, {}, {}, {}".format(self.stockId, self.txDate, self.txCount, self.txAmount, self.txMoney, self.closePrice, self.diffPrice)
        
Base.metadata.create_all(engine)

# operate https://docs.google.com/spreadsheets/d/1033HVmaLyxYkfiX889L5J4ypBuw9xvowotKGPtXWRV0/edit#gid=0
googlesheetService = GooglesheetService("1033HVmaLyxYkfiX889L5J4ypBuw9xvowotKGPtXWRV0")

# get all sheets range name
rangeNameList = googlesheetService.getRangeNameList()

def main():
    
    Session = sessionmaker(bind=engine)
    session = Session()
        
    rows = session.query(StockPrice).distinct(StockPrice.stockId).group_by(StockPrice.stockId)
    for row in rows:
        processStockToGooglesheet(row.stockId)
        
    pass



def processStockToGooglesheet(stockId):
    
    print("process stockId {}...".format(stockId))
    
    # create sheet for stockId if not exist
#     if not stockId in rangeNameList:
#         googlesheetService.addSheet(stockId)
    
    googlesheetService.deleteSheetByRangeName(stockId)

    googlesheetService.addSheet(stockId)
    
    
    header = ["日期","成交股數","成交金額","開盤價","最高價","最低價","收盤價","漲跌價差","成交筆數"]

        

def queryDB(stockId):
    
    Session = sessionmaker(bind=engine)
    session = Session()
      
    rows = session.query(StockPrice).filter_by(stockId=stockId).order_by(StockPrice.id)
    for row in rows:
        print(row)

if __name__ == "__main__":
    main()





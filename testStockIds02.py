'''
寫入公式到 googlesheet 產生所有的基本價格資料

Created on 2018年5月18日
@author: rocky.wang
'''
import csv
from googleService import GooglesheetService

googlesheetService = GooglesheetService("1v_h_IGT9gRYqm1jIf4N413k1KqwGRKwxYx0_ww5Tnz0")

def main():
    
    with open("stockIds.csv", encoding="utf-8") as f1:
        rowList = list(csv.reader(f1))

    cnt2 = 0
    rowNum = 1
    for row in rowList:
        if row[5] != '金融保險業':
            continue
            
        # TODO i cannot handle 上櫃 now
        if row[4] != '上市':
            continue
            
        rowNum += 1
        sheetRow = [row[0], row[1], 
                    '=GOOGLEFINANCE(CONCATENATE("TPE:", $A{}), "price")'.format(rowNum),
                    '=GOOGLEFINANCE(CONCATENATE("TPE:", $A{}), "change")'.format(rowNum),
                    '=GOOGLEFINANCE(CONCATENATE("TPE:", $A{}), "changepct")'.format(rowNum),
                    '=GOOGLEFINANCE(CONCATENATE("TPE:", $A{}), "volume")'.format(rowNum),
                    '=GOOGLEFINANCE(CONCATENATE("TPE:", $A{}), "priceopen")'.format(rowNum),
                    '=GOOGLEFINANCE(CONCATENATE("TPE:", $A{}), "high")'.format(rowNum),
                    '=GOOGLEFINANCE(CONCATENATE("TPE:", $A{}), "low")'.format(rowNum),
                    '=GOOGLEFINANCE(CONCATENATE("TPE:", $A{}), "pe")'.format(rowNum),
                    ]
        
        print(row)

if __name__ == "__main__":
    main()

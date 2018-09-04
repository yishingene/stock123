'''
Created on 2018年3月29日
@author: rocky.wang
'''
import lineTool
import os
from requests.exceptions import ChunkedEncodingError
import time

msg = """2888 新光金 107/08/30 16:00:59 新光金代子公司新光人壽公告取得CDIB Capital Global  Opportunities Fund L.P.

1.標的物之名稱及性質（屬特別股者，並應標明特別股約定發行條件，
如股息率等）:
(1)CDIB Capital Global Opportunities Fund L.P.
(2)私募基金
2.事實發生日:107/08/30
3.交易單位數量、每單位價格及交易總金額:
(1) CDIB Capital Global Opportunities Fund L.P.為合夥組織無交易數量及單位交易
價格
(2)總交易金額為:8,000,000美元
4.交易相對人及其與公司之關係（交易相對人如屬自然人，且非公司
之關係人者，得免揭露其姓名）:
(1) CDIB Capital International Corporation (2)不適用
5.交易相對人為關係人者，並應公告選定關係人為交易對象之原因及
前次移轉之所有人、前次移轉之所有人與公司及交易相對人間相互之
關係、前次移轉日期及移轉金額:
不適用
6.交易標的最近五年內所有權人曾為公司之關係人者，尚應公告
關係人之取得及處分日期、價格及交易當時與公司之關係:
不適用
7.本次係處分債權之相關事項（含處分之債權附隨擔保品種類、處分
債權如有屬對關係人債權者尚需公告關係人名稱及本次處分該關係人
之債權帳面金額:
不適用
8.處分利益（或損失）（取得有價證券者不適用）（遞延者應列表
說明認列情形）:
不適用
9.交付或付款條件（含付款期間及金額）、契約限制條款及其他重要
約定事項:
(1)依基金通知進行認購，總交易金額8,000,000美元; (2)依據基金申購約定
10.本次交易之決定方式、價格決定之參考依據及決策單位:
(1)依基金申購書約定; (2)合夥組織基金無單位價格; (3)依本公司核決權限
11.取得或處分有價證券標的公司每股淨值:不適用
12.有價證券標的公司私募參考價格與每股交易金額差距達20%以上:不適用
13.迄目前為止，累積持有本交易證券（含本次交易）之數量、金額、
持股比例及權利受限情形（如質押情形）:
(1) 基金為合夥組織，無交易數量; (2)8,000,000美元; (3)約6.45%; (4)無
14.迄目前為止，私募有價證券投資（含本次交易）占公司最近期財
務報表中總資產及歸屬於母公司業主之權益之比例暨最近期財務報表中營運資金數額:
(1)占總資產比率: 0.18%(2)占股東權益比率: 4.72%(3)不適用
15.經理人及經紀費用:
無
16.取得或處分之具體目的或用途:
依保險法之規定，為壽險資金之運用"""



def notifyLineMsg(token, msg, retry=2):
    print("retry times", retry)
    try:
        lineTool.lineNotify(token, msg)
    except ChunkedEncodingError as e:
        print(e)
        retry = retry - 1
        msg = msg[0: len(msg)-1]
        if retry > 0:
            time.sleep(1)
            notifyLineMsg(token, msg, retry)
        else:
            raise e
    
notifyLineMsg(os.environ["LINE_TEST_TOKEN"], msg)
    
    





import pandas as pd
import numpy as np
import time
from datetime import datetime

def RSI(close, period=12):
    # 整理資料
    Close = close[-13:]
    Chg = Close - Close.shift(1)
    Chg_pos = pd.Series(index=Chg.index, data=Chg[Chg>0])
    Chg_pos = Chg_pos.fillna(0)
    Chg_neg = pd.Series(index=Chg.index, data=-Chg[Chg<0])
    Chg_neg = Chg_neg.fillna(0)
    
    # 計算平均漲跌幅度
    up_mean = np.mean(Chg_pos.values[-12:])
    down_mean = np.mean(Chg_neg.values[-12:])
    
    # 計算 RSI
    if (up_mean + down_mean > 0):
        rsi = 100 * up_mean / ( up_mean + down_mean )
    else:
        rsi = -1
    
    return rsi

contracts = [api.Contracts.Futures['TXFJ0']]

# 初始化 close series
minute_close = pd.Series()
stock = 0

# 紀錄前12個close
for i in range(0,12):
    snapshots = api.snapshots(contracts)
    minute_close = minute_close.append(pd.Series(
        [snapshots[0].close], 
        index=[pd.to_datetime(snapshots[0].ts, unit='ns')]
    ))
    time.sleep(60)

# 開始算RSI
for i in range(0,700):
    # 抓snapshot
    snapshots = api.snapshots(contracts)
    
    # 存到分k收盤價的series
    minute_close = minute_close.append(pd.Series(
        [snapshots[0].close], 
        index=[pd.to_datetime(snapshots[0].ts, unit='ns')]
    ))
    
    # 計算rsi
    rsi = RSI(minute_close)

    # 觸發訊號判斷
    if rsi <= 30 and rsi >= 0 and stock == 0:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Current Time =", current_time, "BUY AT ", snapshots[0].close)
        stock += 1
    if rsi >= 70 and stock == 1:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Current Time =", current_time, "SELL AT ", snapshots[0].close)
        stock -= 1
    time.sleep(60)
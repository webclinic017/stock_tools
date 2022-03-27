# 串接API取資料
import os
import pandas_datareader as pdr
SPY = pdr.get_data_tiingo('SPY', api_key='YOUR API KEY')
SPY = SPY.reset_index(level=[0,1])
SPY.index = SPY['date']
SPY_adj = SPY.iloc[:,7:12]
SPY_adj.columns = ['Close','High','Low','Open','Volume']

# 篩選2019年收盤價資料
Close = SPY_adj.Close
Close2019 = Close['2019']

# RSI函數
def RSI(Close, period=12):
    # 整理資料
    import pandas as pd
    Chg = Close - Close.shift(1)
    Chg_pos = pd.Series(index=Chg.index, data=Chg[Chg>0])
    Chg_pos = Chg_pos.fillna(0)
    Chg_neg = pd.Series(index=Chg.index, data=-Chg[Chg<0])
    Chg_neg = Chg_neg.fillna(0)
    
    # 計算平均漲跌幅度
    import numpy as np
    up_mean = []
    down_mean = []
    for i in range(period+1, len(Chg_pos)+1):
        up_mean.append(np.mean(Chg_pos.values[i-period:i]))
        down_mean.append(np.mean(Chg_neg.values[i-period:i]))
    
    # 計算 RSI
    rsi = []
    for i in range(len(up_mean)):
        rsi.append( 100 * up_mean[i] / ( up_mean[i] + down_mean[i] ) )
    rsi_series = pd.Series(index = Close.index[period:], data = rsi)
    return rsi_series

# 觀察2019年的RSI14
import matplotlib.pyplot as plt
RSI14_2019 = RSI(Close2019, 14)
plt.plot(RSI14_2019)
plt.title('2019年 RSI14')
plt.axhline(y=80, color='red')
plt.axhline(y=30, color='green')


# 策略： RSI14 < 30 買進，RSI14 > 80 賣出

# 訊號標籤
sig = []

# 庫存標籤，只會是0或1，表示每次交易都是買進或賣出所有部位
stock = 0

# 偵測RSI14訊號
for i in range(len(RSI14_2019)):
    if RSI14_2019[i] > 80 and stock == 1:
        stock -= 1
        sig.append(-1)
    elif RSI14_2019[i] < 30 and stock == 0:
        stock += 1
        sig.append(1)
    else:
        sig.append(0)
# 將訊號整理成dataframe
rsi_sig = pd.Series(index = RSI14_2019.index, data = sig)


import numpy as np
from matplotlib import gridspec
import pandas as pd

fig = plt.figure(figsize=(15,10))
# set height ratios for sublots
gs = gridspec.GridSpec(2, 1, height_ratios=[2, 1]) 

# the fisrt subplot
ax0 = plt.subplot(gs[0])
# line0 = ax0.plot(x, y, color='r')
ax0.plot(RSI14_2019)
ax0.axhline(y=80, color='red')
ax0.axhline(y=30, color='green')

#the second subplot
# shared axis X
ax1 = plt.subplot(gs[1], sharex = ax0)
rsi_sig = pd.Series(index = rsi_sig.index, data = list(rsi_sig.values))
ax1.plot(rsi_sig)

# 回測2019年 RSI14訊號 績效
# 取開盤價資料做回測，因為我們是在前一天收盤後看到訊號，隔天開盤才能買進
Open = SPY_adj.Open
Open2019 = Open['2019']

# 每次買賣的報酬率
rets = []
# 是否仍有庫存
stock = 0
# 當次交易買入價格
buy_price = 0
# 當次交易賣出價格
sell_price = 0
# 每次買賣的報酬率
for i in range(len(rsi_sig)):
    if rsi_sig[i] == 1:
        # 隔日開盤買入
        buy_price = Open2019[rsi_sig.index[i+1]]
        stock += 1
    elif rsi_sig[i] == -1:
        # 隔日開盤賣出
        sell_price = Open2019[rsi_sig.index[i+1]]
        stock -= 1
        rets.append((sell_price-buy_price)/buy_price)
        # 清除上次買賣的價格
        buy_price = 0
        sell_price = 0
# 總報酬率
total_ret = 1
for ret in rets:
    total_ret *= 1 + ret
print(str(round((total_ret - 1)*100,2)) + '%')
# 串接tiingo api獲取資料
import os
import pandas_datareader as pdr
SPY = pdr.get_data_tiingo('SPY', api_key='YOUR API KEY')
SPY = SPY.reset_index(level=[0,1])
SPY.index = SPY['date']
SPY_adj = SPY.iloc[:,7:12]
SPY_adj.columns = ['Close','High','Low','Open','Volume']

# 整理資料
import pandas as pd
# 收盤價
Close = SPY_adj.Close
# 日漲跌
Chg = Close - Close.shift(1)
# 上漲幅度
Chg_pos = pd.Series(index=Chg.index, data=Chg[Chg>0])
Chg_pos = Chg_pos.fillna(0)
# 下跌幅度(取正值，所以要加負號)
Chg_neg = pd.Series(index=Chg.index, data=-Chg[Chg<0])
Chg_neg = Chg_neg.fillna(0)


# 計算12日平均漲跌幅度
import numpy as np
up_mean_12 = []
down_mean_12 = []
for i in range(13,len(Chg_pos)+1):
    up_mean_12.append(np.mean(Chg_pos.values[i-12:i]))
    down_mean_12.append(np.mean(Chg_neg.values[i-12:i]))

# 計算 RSI12
rsi_12 = []
for i in range(len(up_mean_12)):
    rsi_12.append( 100 * up_mean_12[i] / ( up_mean_12[i] + down_mean_12[i] ) )
rsi_12_series = pd.Series(index = Close.index[12:], data = rsi_12)

# RSI函數
def RSI(Close, period=12):
    # 整理資料
    import pandas as pd
    Chg = Close - Close.shift(1)
    Chg_pos = pd.Series(index=Chg.index, data=Chg[Chg>0])
    Chg_pos = Chg_pos.fillna(0)
    Chg_neg = pd.Series(index=Chg.index, data=-Chg[Chg<0])
    Chg_neg = Chg_neg.fillna(0)
    
    # 計算12日平均漲跌幅度
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

# 稍微對照一下剛剛算出來的數字，會是一樣的
RSI(Close)



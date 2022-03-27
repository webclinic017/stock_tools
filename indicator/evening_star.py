# 串接API抓取資料
import os
import pandas_datareader as pdr
SPY = pdr.get_data_tiingo('SPY', api_key='YOUR API KEY')
SPY = SPY.reset_index(level=[0,1])
SPY.index = SPY['date']
SPY_adj = SPY.iloc[:,7:11]
SPY_adj.columns = ['Close','High','Low','Open']

# 取2019年的數據
SPY_adj_2019 = SPY_adj['2019']

# 開盤價 & 收盤價
SPY_adj_2019_Open = SPY_adj_2019.Open
SPY_adj_2019_Close = SPY_adj_2019.Close

# 當日漲跌點數
SPY_DailyChg_2019 = SPY_adj_2019_Close - SPY_adj_2019_Open

# 取得每日的振幅
SPY_Abs_DailyChg_2019 = abs(SPY_DailyChg_2019)

# 分析振幅統計數據，以利篩選適合的K棒
SPY_Abs_DailyChg_2019.describe()

# 抓取 第1根大振幅陽線、第2根小振幅陽線或陰線、第3根陰線且振幅大於第1根的1/2
evening_condition_1 = [0,0]
for i in range(2, len(SPY_DailyChg_2019)):
    if ( SPY_DailyChg_2019[i-2] > 1.158 ) & ( abs(SPY_DailyChg_2019[i-1]) < 0.388 ) & ( SPY_DailyChg_2019[i] < -0.58 ):
        evening_condition_1.append(1)
    else:
        evening_condition_1.append(0)

# condition 1 符合的次數
evening_condition_1.count(1)

# 第2根的開盤與收盤價 均大於 第1根的收盤與第3根的開盤
evening_condition_2 = [0,0]
for i in range(2, len(SPY_adj_2019_Open)):
    if ( SPY_adj_2019_Open[i-1] > SPY_adj_2019_Close[i-2] ) & ( SPY_adj_2019_Open[i-1] > SPY_adj_2019_Open[i] ) & ( SPY_adj_2019_Close[i-1] > SPY_adj_2019_Close[i-2] ) & ( SPY_adj_2019_Close[i-1] > SPY_adj_2019_Open[i] ):
        evening_condition_2.append(1)
    else:
        evening_condition_2.append(0)
evening_condition_2.count(1)

# Evening Star Signal
evening_star_signal = []
for i in range(len(evening_condition_1)):
    if ( evening_condition_1[i] == 1 ) & ( evening_condition_2[i] == 1 ):
        evening_star_signal.append(1)
    else:
        evening_star_signal.append(0)
        
# Find Evening Star date
for i in range(len(evening_star_signal)):
    if evening_star_signal[i] == 1:
        print(SPY_adj_2019.index[i])

# 檢視K線圖
import mplfinance as mpf

SPY_adj_2019_Aug = SPY_adj_2019['2019-08']
mpf.plot(SPY_adj_2019_Aug,type='candle')

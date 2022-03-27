import os
import pandas_datareader as pdr
SPY = pdr.get_data_tiingo('SPY', api_key='YOUR API KEY')
SPY = SPY.reset_index(level=[0,1])
SPY.index = SPY['date']
SPY_adj = SPY.iloc[:,7:11]
SPY_adj.columns = ['Close','High','Low','Open']

# 使用開盤價計算報酬率
SPY_Open_adj = SPY_adj.Open

# 看到訊號後隔天交易，買完隔1日賣/買完隔5日賣 的報酬率
ret1 = SPY_Open_adj.shift(-2) / SPY_Open_adj.shift(-1)

ret5 = SPY_Open_adj.shift(-6) / SPY_Open_adj.shift(-1)


def Evening_Star_Sig(data):
    # 開盤價/收盤價
    data_Open = data.Open
    data_Close = data.Close
    
    # 當日漲跌
    data_DailyChg = data_Close - data_Open
    
    # 取得每日的振幅
    data_Abs_DailyChg = abs(data_DailyChg)
    
    # 計算統計數據
    mean = data_Abs_DailyChg.mean()
    first_quar = data_Abs_DailyChg.quantile(q=0.25)
    
    # 抓取 第1根大振幅陽線、第2根小振幅陽線或陰線、第3根陰線且振幅大於第1根的1/2
    evening_condition_1 = [0,0]
    for i in range(2, len(data_DailyChg)):
        if ( data_DailyChg[i-2] > mean ) & ( abs(data_DailyChg[i-1]) < first_quar ) & ( data_DailyChg[i] < -0.5*mean ):
            evening_condition_1.append(1)
        else:
            evening_condition_1.append(0)
            
    # 第2根的開盤與收盤價 均大於 第1根的收盤與第3根的開盤
    evening_condition_2 = [0,0]
    for i in range(2, len(data_Open)):
        if ( data_Open[i-1] > data_Close[i-2] ) & ( data_Open[i-1] > data_Open[i] ) & ( data_Close[i-1] > data_Close[i-2] ) & ( data_Close[i-1] > data_Open[i] ):
            evening_condition_2.append(1)
        else:
            evening_condition_2.append(0)
            
    # Evening Star Signal
    evening_star_signal = []
    for i in range(len(evening_condition_1)):
        if ( evening_condition_1[i] == 1 ) & ( evening_condition_2[i] == 1 ):
            evening_star_signal.append(1)
        else:
            evening_star_signal.append(0)
            
    # Return a boolean series
    import pandas as pd
    sig = pd.Series(index = data.index, data = evening_star_signal)
    sig = sig.astype('bool')
    return sig

# 抓取 Evening star訊號
sig = Evening_Star_Sig(SPY_adj)

ret1[sig].mean()

ret5[sig].mean()

# 回測 Evening star出現後，買賣間隔1~100天的平均報酬率
rets = []
for i in range(2,102):
    ret = SPY_Open_adj.shift(-i) / SPY_Open_adj.shift(-1)
    rets.append(ret[sig].mean())
    
# 畫出天數對應報酬率的圖
import pandas as pd
import matplotlib.pyplot as plt
ret_df = pd.DataFrame(index=range(1,101),data=rets)
ret_df.columns = ['return']
ret_df = (ret_df-1) * 100
plt.figure(figsize=(12,8))
plt.plot(ret_df)
plt.hlines(y=0, xmin=0, xmax=100, color='red')
plt.title("平均報酬率 v.s. 買賣間隔時間",fontsize=15)
plt.xlabel("買賣間隔天數(天)", fontsize=15)
plt.ylabel("平均報酬率(%)", fontsize=15)


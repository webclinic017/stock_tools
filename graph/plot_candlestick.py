# 取得Google股票的價格，美股代號GOOG
import os
import pandas_datareader as pdr
import yaml

with open("../secret.yaml", "r") as stream:
    try:
        data = yaml.safe_load(stream)
        tiingo_key = data['tiingo_api_key']
    except yaml.YAMLError as exc:
        print(exc)
        exit()


df = pdr.get_data_tiingo('GOOG', api_key=tiingo_key)
df.tail()

# 將multi-index轉成single-index
df = df.reset_index(level=[0,1])

# 指定date為index
df.index = df['date']

# 取adjClose至adjOpen的欄位資料
df_adj = df.iloc[:,7:11]

# 更改columns的名稱，以讓mplfinance看得懂
df_adj.columns = ['Close','High','Low','Open']

# 抓取近20日的資料
df_adj_20d = df_adj.iloc[-20:,:]

# 繪製K線圖
import mplfinance as mpf
mpf.plot(df_adj_20d)

mpf.plot(df_adj_20d,type='candle')

mpf.plot(df_adj_20d,type='line')
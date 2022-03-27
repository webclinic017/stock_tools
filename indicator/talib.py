import numpy
import talib
# 看一下全部的函數，https://mrjbq7.github.io/ta-lib/funcs.html
all_functions = talib.get_functions()
print(len(all_functions))
print(all_functions)

all_groups = talib.get_function_groups()
print(len(all_groups))
print(all_groups)

import os
import pandas_datareader as pdr
SPY = pdr.get_data_tiingo('SPY', api_key='your api key')
SPY = SPY.reset_index(level=[0,1])
SPY.index = SPY['date']
SPY_adj = SPY.iloc[:,7:12]
SPY_adj.columns = ['Close','High','Low','Open','Volume']

# K pattern recognition
EVENINGSTAR = talib.CDLEVENINGSTAR(SPY_adj.Open.values,SPY_adj.High.values,SPY_adj.Low.values,SPY_adj.Close.values)
EVENINGSTAR[EVENINGSTAR!=0]
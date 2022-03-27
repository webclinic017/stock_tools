# binance trade bot
from sys import last_traceback
import pandas as pd
import datetime
import requests
import time
import calendar
from pybit import HTTP
from datetime import datetime, timedelta, timezone
import os

from sklearn.metrics import average_precision_score

#apiKey = os.getenv('bybit_testnet_api')
api_key = 1234
api_secret=1234

symbol='BTCUSD'

tick_interval = '1'

qtyl=10

while True:

    bybitticker=symbol
    print(symbol)

    now = datetime.utcnow()
    unixtime = calendar.timegm(now.utctimetuple())
    since = unixtime

    start = str(since-60*60*int(tick_interval))

    url = 'https://testnet.bybit.com/api/v2/public/kline/list?symbol='+bybitticker+'&interval='+tick_interval+'&from='+str(start)
    
    data = requests.get(url).json()
    D = pd.DataFrame(data['result'])

    marketprice = 'https://testnet.bybit.com/api/v2/public/tickers?symbol='+bybitticker
    res = requests.get(marketprice)
    data = res.json()
    lastprice = float(data['result'][0]['last_price'])

    price = lastprice

    df = D['close']

    ma9 = df.rolling(9).mean()
    ma26 = df.rolling(26).mean()

    test1 = ma9.iloc[-2] - ma26.iloc[-2]
    test2 = ma9.iloc[-1] - ma26.iloc[-1]

    session = HTTP(
        endpoint="https://testnet.bybit.com",
        api_key=api_key,
        api_secret=api_secret)

    # do it later







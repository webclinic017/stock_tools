import pandas as pd
from pandas.core.algorithms import quantile
import datatime as dt
from binance.client import ???
import time
import numpy
import requests

# bollingerband

def bollingerband(symbol, width, intervalunit, length):

    if intervalunit == "1T":

        start_str = "100 minutes ago UTC"
        interval_date = '1m'

        D = pd.DataFrame(client.get_historical_klines(symbol=symbol, start_str = start_str, interval=interval_date))
        D.columns = ['open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'qav', 'num'
            'taker_base_vol', 'taker_quote_vol', 'is_best_math']
        D['open_date_time'] = [dt.datetime.fromtimestamp(x/1000) for x in D.open_time]
        D['symbol']= symbol
        
        D = D[['symbol', 'open_date_time', 'open', 'high', 'low', 'close', 'volume', 'num_trades', 'taker_base_vol',
              'taker_quote_vol']]

    df = D.set_index('open_date_time')

    df['close'] = df['close'].astype(float)

    df = df['close']

    df1 = df.resample(intervalunit).agg({
       "close": "last" 
    })

    unit = width

    band1 = unit * numpy.std(df1['close'][len(df1) - length: len(df1)])

    bb_center = numpy.mean(df1['close'][len(df1) - length: len(df1)])

    band_high = bb_center + band1

    band_low = bb_center - band1

    return band_high, bb_center, band_low,

while True:

    # api key
    api_key = api_key
    api_secret = api_secret

    client = Client(api_key=api_key, api_secret=api_secret)

    symbol_trade="XRPBUSD"

    orderquantity=35

    length=20
    width=2

    bb_lm = bollingerband(sumbol_trade, width, '1T', length)

    print("1 minute upper center lower: ", bb_1m)

    marketplace = "https://api.binance.com/api/v1/ticker/24hr?symbol=" + symbol_trade
    res = requests.get(marketprice)
    data - res.json()
    lastprice = float(data['lastPrice'])

    print(lastprice)

    try:

        if lastprice > bb_lm[0]:
            print('sell')
            client.order_market_sell(symbol=symbol_trade, quantity=orderquantity)
            break  #stop the loop as order has been made.

    except:
        pass

    try:
        if lastprice < bb_lm[2]:
            print('buy')
            client.order_market_buy(symbol=symbol_trade, quantity=orderquantity)
            break # stop the loop if the order is made
    except:
        pass

    time.sleep(1)
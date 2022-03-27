# https://algotrading101.com/learn/alpaca-trading-api-guide/
# alpaca is good, but not as good as cryptowatchand poocoin for the time being
import alpaca_trade_api as tradeapi
import yaml
import pandas as pd
from datetime import datetime, timedelta

# read from secret
with open("../secret.yaml", "r") as stream:
    try:
        data = yaml.safe_load(stream)
        alpaca_paper_endpoint = data['alpaca_paper_endpoint']
        alpaca_api_key = data['alpaca_api_key']
        alpaca_api_secret = data['alpaca_api_secret']

    except yaml.YAMLError as exc:
        print(exc)
        exit()

api = tradeapi.REST(alpaca_api_key, alpaca_api_secret, alpaca_paper_endpoint, api_version='v2')
d = datetime.today()
starttime = '%d-%02d-%02dT09:30:00-05:00' % (d.year, d.month, d.day)
endtime = '%d-%02d-%02dT16:00:00-05:00' % (d.year, d.month, d.day)


#btc (ok)
barset = api.get_crypto_bars('BTCUSD', '15Min', limit=960, start=starttime, end=endtime)
print(barset)
 
#eth (ok)
barset = api.get_crypto_bars('ETHUSD', '15Min', limit=960, start=starttime, end=endtime)
print(barset)

#bsc (not ok)
barset = api.get_crypto_bars('BNBUSD', '15Min', limit=960, start=starttime, end=endtime)
print(barset)


#sol
barset = api.get_crypto_bars('SOLUSD', '15Min', limit=960, start=starttime, end=endtime)
print(barset)

#aave
barset = api.get_crypto_bars('AAVEUSD', '15Min', limit=960, start=starttime, end=endtime)
print(barset)
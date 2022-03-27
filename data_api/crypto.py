# This is the crypto module
# Extract coin info from either cryptowatch or pancakeswap

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from datetime import datetime, timedelta
import pandas as pd
from . import coingecko
from . import cryptowatch


def get_olhc(symbol: str, date_from: datetime, date_to: datetime):
    '''
    Multiple provider: cryptowatch, pancake swap api, and also coingecko.
    '''
    # try:
    #     return getOlhcFromCryptoWatch(symbol, date_from, date_to)
    # except:
    #     return getOlhcFromPancakeSwapApi(symbol)
    
    # if both date_from and date_to are within 30 day of today, use coingecko, else use cryptowatch
    date_30_before = datetime.today().date() + timedelta(days=-30)
    if date_from >= date_30_before:
        df =  coingecko.get_olhc(symbol, abs((date_from - datetime.today().date()).days))
        if not df is None:
            df = df.loc[date_from:date_to]
        return df
    else:
        try:
            return cryptowatch.get_olhc(symbol, date_from, date_to)
        except:
            return None
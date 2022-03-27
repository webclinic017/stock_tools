# This is the stock module
# Extract coin info from either cryptowatch or pancakeswap
import pandas as pd
from . import alphavantage
from . import alpaca
from datetime import datetime

def __get_olhc_us(symbol: str, date_from: datetime, date_to: datetime):
    return alpaca.get_olhc(symbol, date_from, date_to)

def __get_olhc_hk(symbol: str, date_from: datetime, date_to: datetime):
    pass

def get_olhc(symbol: str, date_from: datetime, date_to: datetime, region: str):
    if region.lower() == "us":
        return __get_olhc_us(symbol, date_from, date_to)
    elif region.lower() == "hk":
        return __get_olhc_hk(symbol, date_from, date_to)
    else: 
        raise ValueError("region not yet supported.")

def __get_fundamentals_us(symbol):
    return alphavantage.get_fundamental(symbol)

def __get_fundamentals_hk(symbol):
    pass

def get_fundamentals(symbol, region):
    if region.lower() == "hk":
        return __get_fundamentals_hk(symbol)
    elif region.lower() == "us":
        return __get_fundamentals_us(symbol)
    else: 
        raise ValueError("region not yet supported.")

def get_option_chart(symbol, region):
    pass

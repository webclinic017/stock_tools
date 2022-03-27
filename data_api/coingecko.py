from math import e
from socketserver import ForkingMixIn
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from datetime import datetime, timedelta
from . import utilities

def __symbol_to_id(symbol: str):
    gecko_id = {
        'eth': 'ethereum',
        'bnb': 'binancecoin',
        'ceek': 'ceek', 
        'bit': 'bitdao',
        'usdt': 'tether',
        'busd': 'binance-usd',
        'kasta': 'kasta',
        'thc': 'thetan-coin',
        'pi': '???',
        'sol': 'solana',
        'aca': 'acala',
        'matic': 'matic-network',
        'bdot': 'binance-wrapped-dot',
        'weth-polygon': 'ethereum',
    }

    return gecko_id.get(symbol.lower())


def get_all_symbol():
    url = 'https://api.coingecko.com/api/v3/coins/list'
    #print(symbol, url)

    headers = {
        'Accepts': 'application/json',
    }

    params = {
        'include_platform': "true",
    }
    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=params)
        data = json.loads(response.text)
        print(response.text)
        f = open("gecko.txt", "r", encoding='UTF-8')
        f.write(json.dumps(data))
        f.close()
    except:
        pass

def read_olhc():
    f = open('gecko_olhc.txt',)
    data = json.load(f)

    for i in data:
        print(i)


def get_olhc(symbol: str, days: int):
    '''
    from: https://www.coingecko.com/zh/api/documentation?__cf_chl_jschl_tk__=de.CxkBvFf7M.PljTfKXApzLNgZA_hcVoNIp9TVAQWw-1641851212-0-gaNycGzNChE
    Candle's body:

    1 - 2 days: 30 minutes
    3 - 30 days: 4 hours
    31 and before: 4 days
    1/7/14/30/90/180/365/max
    '''

    url = 'https://api.coingecko.com/api/v3/coins/%s/ohlc' % __symbol_to_id(symbol)

    headers = {
        'Accepts': 'application/json',
    }

    value_days =[1,7,14,30,90,180,365]

    if days > 365:
            days = "max"
    else:
        for v in value_days:
            if days <= v:
                days = v
                break
    

    params = {
        'vs_currency': "usd",
        'days': days, 
    }
    session = Session()
    session.headers.update(headers)

    try:
        df = utilities.get_olhc_df()
        
        response = session.get(url, params=params)
        data = json.loads(response.text)

        for rec in data: 
            rec_time = datetime.utcfromtimestamp(rec[0]/1000)

            df = df.append({
                'Close': rec[4] ,'High': rec[2], 'Low': rec[3], 'Open': rec[1], 'Time': rec_time, 'Volume': 0 
            }, ignore_index=True)

        df.set_index('Time', inplace=True)
        df = utilities.resample_df(df)
        return df
    except Exception as e:
        print(e)
        pass


if __name__ == '__main__':

    query_crypto = ['binancecoin', 'ethereum', 'solana', 'avalanche-2']
    start_date = datetime.today() + timedelta(days=-14)
    end_date = datetime.today()

    for symbol in query_crypto:
        df_bar = get_olhc(symbol, 14)

        print(df_bar)
        # download and save it to other place
        #df_bar.to_csv('%s_%s.csv' % (symbol, datetime.today().strftime("%Y-%m-%d")))
        
        break

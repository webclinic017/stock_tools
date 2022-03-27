
import yaml
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from datetime import datetime, timedelta
import pandas as pd
from . import utilities
import os

def get_olhc(crypto_symbol, start_date, end_date, period=86400):

    # read from secret
    secret_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "secret.yaml")
    with open(secret_path, "r") as stream:
        try:
            data = yaml.safe_load(stream)
            cryptowatch_public_key = data['cryptowatch_public_key']

        except yaml.YAMLError as exc:
            print(exc)
            exit()

    df_bar = utilities.get_olhc_df()

    url = 'https://api.cryptowat.ch/markets/binance-us/%susd/ohlc' %  crypto_symbol
    #print(symbol, url)

    headers = {
        'Accepts': 'application/json',
        'X-CW-API-Key': cryptowatch_public_key,
    }

    params = {
        'after': int(datetime.timestamp(start_date)),
        'before': int(datetime.timestamp(end_date)),
        'periods' : period,
    }
    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=params)
        data = json.loads(response.text)
        
        print(json.dumps(data))
        # download and save it to other place
        for rec in data["result"]["86400"]:
            date_rec = datetime.utcfromtimestamp(rec[0])
            df_bar = df_bar.append({'Close': rec[4], 'High': rec[2], 'Low': rec[3], 'Open': rec[1], 'Time': date_rec, 'Volume': rec[6],}, ignore_index=True)

        df_bar.set_index('Time', inplace=True)

        return df_bar

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

if __name__ == '__main__':
    
    query_crypto = ['MATIC', 'ETH', 'SOL', 'AVAX']
    start_date = datetime.today() + timedelta(days=-14)
    end_date = datetime.today()

    for symbol in query_crypto:
        df_bar = get_olhc(symbol, start_date, end_date)

        # download and save it to other place
        df_bar.to_csv('%s_%s.csv' % (symbol, datetime.today().strftime("%Y-%m-%d")))
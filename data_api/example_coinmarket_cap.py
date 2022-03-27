
import yaml
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from datetime import datetime, timedelta

# read from secret
with open("../secret.yaml", "r") as stream:
    try:
        data = yaml.safe_load(stream)
        coinmarketcap_api = data['coinmarketcap_api_key']

    except yaml.YAMLError as exc:
        print(exc)
        exit()

query_crypto = ['BNB', 'ETH', 'SOL', 'AVAX']

# find all the market id

# url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map'
# parameters = {
#   'symbol':','.join(query_crypto),
# }
# headers = {
#   'Accepts': 'application/json',
#   'X-CMC_PRO_API_KEY': coinmarketcap_api,
# }
# session = Session()
# session.headers.update(headers)

# try:
#   response = session.get(url, params=parameters)
#   data = json.loads(response.text)
#   print(data)
# except (ConnectionError, Timeout, TooManyRedirects) as e:
#   print(e)

#get info related to last day and ATR

start_date = datetime.today()+ timedelta(days= -5)
end_date = datetime.today()

## What the heck, basic plan does not have historical data?
for sym in query_crypto:

    # crypto_data = data.filter(lambda x:  x.symbol == sym)

    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/ohlcv/historical'
    parameters = {
    'symbol': sym, 
    'time_period':'daily',
    'time_start': start_date.strftime("%Y-%m-%d"),
    'time_end':end_date.strftime("%Y-%m-%d"),
    }
    headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': coinmarketcap_api,
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        print(data)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
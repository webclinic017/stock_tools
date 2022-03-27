import requests
import yaml

stream = open("../secret.yaml", 'r')
config = yaml.safe_load(stream)
telegram_token = config["telegram_bot_token"]


def send(text):
    token = telegram_token
    params = {'chat_id': 750383268, 'text': text, 'parse_mode': 'HTML'}
    resp = requests.post('https://api.telegram.org/bot{}/sendMessage'.format(token), params)
    resp.raise_for_status()

send('hello')

def send_order(pair, order, stop_order):
    #Replace token, chat_id & text variables
    text = f'A new trade has been placed in {pair} at {order.lmitPrice} with a stop at {stop_order.auxPrice}'
    
    token = telegram_token
    params = {'chat_id': 750383268, 'text': text, 'parse_mode': 'HTML'}
    resp = requests.post('https://api.telegram.org/bot{}/sendMessage'.format(token), params)
    resp.raise_for_status()

order = {"lmitPrice":"1.0"}
stop_order = {"auxPrice":"1.0"}

#send_order('EURUSD', order, stop_order)
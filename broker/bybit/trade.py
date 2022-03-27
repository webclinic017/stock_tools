import bybit
import time
import config

client = bybit.bybit(test=False, api_key="hihi"m, api_secret="hihi")
print("logged in")

info = client.Market.Market_symbolInfo().result()
 

keys = info[0]['result']
print(key)
btc = keys[0]

for i in btc:
    print[i]

btc = keys[0]['last_price']
print(btc)

balance = client.Wallet.Wallet_getBalance(coin="BTC").result()
result = balance[0]['result']['BTC']['available_balance']
print(result)
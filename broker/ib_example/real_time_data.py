import shioaji as sj
import json
# api init
api = sj.Shioaji(backend='https', simulation=False)

# login
# 這邊跟之前寫法不太一樣，這次把帳號密碼寫成一個txt檔再去讀它
with open('login.txt', 'r') as f:
    kw_login = json.loads(f.read())  
    api.login(**kw_login)

# activate ca
person_id = kw_login['person_id']  
api.activate_ca(ca_path='./Sinopac.pfx', ca_passwd=person_id, person_id=person_id)

# contract
contract = api.Contracts.Stocks["2330"]

# callback 
@api.quote.on_quote
def quote_callback(topic: str, quote: dict):
    print(f"Topic: {topic}, Quote: {quote}")


# subscribe tick data
api.quote.subscribe(contract, quote_type=sj.constant.QuoteType.Tick)

# unsubscribe tick data
api.quote.unsubscribe(contract, quote_type=sj.constant.QuoteType.Tick)

# subscribe Bid Ask
api.quote.subscribe(contract, quote_type=sj.constant.QuoteType.BidAsk)

# 可以同時訂閱多組快照
contracts = [api.Contracts.Stocks['2330'], api.Contracts.Stocks['3481']]
snapshots = api.snapshots(contracts)

# 每隔10秒抓一次資料
import time
for i in range(0,4):
    print(snapshots)
    time.sleep(10)
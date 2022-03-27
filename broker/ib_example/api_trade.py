# shioaji seems obsoleted as of 2021

# contract，這邊用台積電作為範例
contract = api.Contracts.Stocks.TSE.TSE2330

#buy
order = api.Order(price=439, 
                  quantity=1, 
                  action="Buy", 
                  price_type="LMT", 
                  order_type="ROD", 
                  order_lot="Common", 
                  account=api.stock_account
                  )

#sell
order = api.Order(price=450, 
                  quantity=1, 
                  action="Sell", 
                  price_type="LMT", 
                  order_type="ROD", 
                  order_lot="Common", 
                  account=api.stock_account
                  )

# API initialization
import shioaji as sj
import json
api = sj.Shioaji(backend='https', simulation=False)

# login
with open('login.txt', 'r') as f:
    kw_login = json.loads(f.read())  
    api.login(**kw_login)

# activate ca
person_id = kw_login['person_id']  
api.activate_ca(ca_path='./Sinopac.pfx', ca_passwd=person_id, person_id=person_id)

contract = api.Contracts.Stocks.TSE.TSE2330
order = api.Order(price=400, 
                  quantity=1, 
                  action="Buy", 
                  price_type="LMT", 
                  order_type="ROD", 
                  order_lot="Common", 
                  account=api.stock_account
                  )
trade = api.place_order(contract, order)

api.update_status(api.stock_account)
api.cancel_order(trade)
api.update_status(api.stock_account)


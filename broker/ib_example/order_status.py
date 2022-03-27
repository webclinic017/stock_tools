#order

contract = api.Contracts.Stocks.TSE.TSE2330
order = api.Order(price=400,
                  quantity=1,
                  action="Buy",
                  price_type="LMT",
                  order_type="ROD",
                  account=api.stock_account
                  )
trade = api.place_order(contract, order)

#cancel
api.cancel_order(trade)

#update order price
api.update_order(trade=trade, price=410)

#update order quantity
# qty是指要減少的數量
api.update_order(trade=trade, qty=1)
# shioaji seems obsoleted as of 2021

api.list_positions(api.stock_account)

import pandas as pd
pl = api.list_profit_loss(api.stock_account,'2020-05-05','2020-09-30')
df = pd.DataFrame(pl)


# 後面那個2就是使用上面Profit Loss的id
detail = api.list_profit_loss_detail(api.stock_account, detail_id = 0)
df = pd.DataFrame(detail)

settlement = api.list_settlements(api.stock_account)
df = pd.DataFrame(settlement)

acc_balance = api.account_balance()
df = pd.DataFrame(acc_balance)
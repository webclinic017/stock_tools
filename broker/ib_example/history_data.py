# 載入shioaji套件
import shioaji as sj

# Initialization
api = sj.Shioaji()

# Login
accounts = api.login("YOUR_PERSON_ID", "YOUR_PASSWORD")

# 載入憑證
api.activate_ca(
    ca_path="/c/your/ca/path/Sinopac.pfx",
    ca_passwd="YOUR_CA_PASSWORD",
    person_id="Person of this Ca",
)

contract_0050 = api.Contracts.Stocks["0050"]
contract_0050

Stock(exchange=<Exchange.TSE: 'TSE'>, code='0050', symbol='TSE0050', name='元大台灣50', category='00', limit_up=115.9, limit_down=94.9, reference=105.4, update_date='2020/09/18', margin_trading_balance=7405, day_trade=<DayTrade.Yes: 'Yes'>)

ticks = api.ticks(contract_0050, "2020-09-18")

import pandas as pd
tick_data_df = pd.DataFrame({**ticks})
tick_data_df.ts = pd.to_datetime(tick_data_df.ts)
tick_data_df.head()

kbars = api.kbars(contract_0050, start="2020-09-18", end="2020-09-18")
kbars_df = pd.DataFrame({**kbars})
kbars_df.ts = pd.to_datetime(kbars_df.ts)
kbars_df.head()

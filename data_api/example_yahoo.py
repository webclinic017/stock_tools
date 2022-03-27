from mailbox import BabylMessage
import pandas as pd
import yfinance as yf
from datetime import datetime
import logging

start_date = '2000-01-01'
end_date = datetime.today().strftime("%Y-%m-%d")

symbols = [
    'DX-Y.NYB',
    'JPY=X',
    'EURGBP=X',
    'AUDNZD=X',
    'NZDCAD=X',
    '^GSPC',
    '000001.SS',
    '^HSI',
    'GC=F',
    'SI=F',
    'CRUD.L',
    'BTC-USD',
    'AAPL',
    'MSFT',
    'BABA', 
    'KO',
    'JPM'
]

symbols = ['000001.SS',]

for i in symbols:
    logging.error("downloading " + i)
    aapl_df = yf.download(i, 
                        start=start_date, 
                        end=end_date, 
                        progress=False,
    )

    aapl_df.to_csv(i+".csv")
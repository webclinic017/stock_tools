from re import S
import sys, importlib
from pathlib import Path
import talib
import os
import arrow
import pysftp
import logging
from io import StringIO
import matplotlib.pyplot as plt

from tom_stock_common.data import stock, crypto, google_api
from tom_stock_common.broker.ib import IB

from datetime import datetime, timedelta

import pandas as pd
import yaml

def __read_config():
    result  = {
        "day_archive": 14, 
        "archive_location": "/Users/yiuminglai/GitProjects/stock_tools/data/private/report",
        "archive_sftp_location": "/Users/yiuminglai/GitProjects/stock_tools/data/private/report",
        "report_location": "/Users/yiuminglai/GitProjects/stock_tools/data/private/report",
        "archive_sftp": "/home/personal_finance",
        "crypto_spreadsheet_id": '1JC5yyhtGaQTBSBEN1-LxF3-YlQM1HkIUO27U06_vUoM', 
        "crypto_spreadsheet_range": 'crypto!A4:C',
        "stock_spreadsheet_id": '1JC5yyhtGaQTBSBEN1-LxF3-YlQM1HkIUO27U06_vUoM', 
        "stock_spreadsheet_range": 'fundamental!A2:C',
        }

    # read sftp secret
    secret_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "secret.yaml")
    with open(secret_path, "r") as stream:
        try:
            data = yaml.safe_load(stream)
            result.update(data)

            #result['synology_sftp_url'] = data['synology_sftp_url']
            #result['synology_sftp_port'] = data['synology_sftp_port']
            #result['synology_username'] = data['synology_username']
            #result['synology_password'] = data['synology_password']
        except yaml.YAMLError as exc:
            print(exc)
            exit()
    # Now read some secret

    return result

def __get_crypto_df():
    result = pd.DataFrame(columns = ['Symbol','Price', 'Total USD', 'ATR'])
    return result

def __get_stock_df():
    result = pd.DataFrame(columns = ['Symbol','Price', 'Position', 'Total USD', 'Unrealized profit',
     'ATR', 'Suggested stop', 'Beta', 'PE', 'Pct.'])
    return result

# Here is the procedure
def __get_crypto_data(config):
    # Read the google spreadsheet, get my crypto assets and then
    values = google_api.read_spreadsheet(config["crypto_spreadsheet_id"], config["crypto_spreadsheet_range"], config)

    crypto_df = __get_crypto_df()

    #get history data to calculate the current price and ATR
    start_date = datetime.today().date() + timedelta(days=-30)
    end_date = datetime.today().date()
    for row in values:
        symbol = row[1] #row 1 is gecko symbol
        amount = float(row[2])
        olhc = crypto.get_olhc(row[0], start_date, end_date, config)
        if not olhc is None:
            price = olhc["Close"].iloc[-1]
            atr_df = talib.ATR(olhc["High"], olhc["Low"], olhc["Close"], timeperiod=14)
            atr = atr_df[-1]
            total_price = price * amount
        else:
            price = 0
            atr = 0
            total_price = 0

        crypto_df = crypto_df.append({"Symbol": symbol, "Price": price, "Total USD": total_price, "ATR": atr,}, ignore_index=True)

    return crypto_df

def __get_stock_data_us(config):
    
    stock_df = __get_stock_df()
    
    start_date = datetime.today().date() + timedelta(days=-30)
    end_date = datetime.today().date()

    ib = IB()
    ib.setup_ib_deamon(config) 
    portfolio = ib.get_account_stock()
    ib.close()

    values = google_api.read_spreadsheet(config["stock_spreadsheet_id"], config["stock_spreadsheet_range"], config)

    fund_dict = {}

    for row in values:
        symbol = row[0]
        beta = float(row[1])
        earning_ttm = float(row[2])
        fund_dict[symbol] = {"beta": beta, "earning_ttm": earning_ttm}

    sc_row = {"Symbol": "Short call", "Price": -1, "Position": -1, "Total USD": 0, 
                'Unrealized profit': 0, "ATR": -1, 'Suggested stop': -1, "Beta": -1, "Pct." : 0}
    sp_row = {"Symbol": "Short put", "Price": -1, "Position": -1, "Total USD": 0, 
                'Unrealized profit': 0, "ATR": -1, 'Suggested stop': -1, "Beta": -1, "Pct." : 0}
    lc_row = {"Symbol": "Long call", "Price": -1, "Position": -1, "Total USD": 0, 
                'Unrealized profit': 0, "ATR": -1, 'Suggested stop': -1, "Beta": -1, "Pct." : 0}
    lp_row = {"Symbol": "Long put", "Price": -1, "Position": -1, "Total USD": 0, 
                'Unrealized profit': 0, "ATR": -1, 'Suggested stop': -1, "Beta": -1, "Pct." : 0}

    for index, row in portfolio.iterrows():
        symbol = row["Symbol"].replace(' ', '.')
        position = float(row["Position"])
        total = row["MarketPrice"] * float(row["Position"])
        unrealized_profit = row["UnrealizedPNL"]

        if row["SecType"] == "STK":
            
            # now get the latest 14 day price
            logging.info("Processing stock symbol: " + symbol)
            print('debug', symbol)
            fund_symbol = fund_dict.get(symbol)
            if fund_symbol is not None:
                beta = fund_symbol["beta"]
            else:
                beta = -1
            try:
                olhc = stock.get_olhc(symbol, start_date, end_date, "US", config) 
            except:
                olhc = None 
            #fund = get_fundamentals(symbol, "US")

            if not olhc is None:
                price = row["MarketPrice"]
                
                if fund_symbol is not None and float(fund_symbol["earning_ttm"]) > 0: 
                    pe = float(row["MarketPrice"]) / float(fund_symbol["earning_ttm"])
                else:
                    pe = 0

                #print(symbol)
                #print(olhc)
                atr_df = talib.ATR(olhc["High"], olhc["Low"], olhc["Close"], timeperiod=14)
                #print(atr_df)
                atr = atr_df[-1]
                suggested_stop = price - atr* 3
            else:
                price = 0
                atr = 0
                suggested_stop = 0
                pe = 0

            stock_df = stock_df.append({"Symbol": symbol, "Price": price, "Position": position, "Total USD": total, 
                'Unrealized profit': unrealized_profit, "ATR": atr, 'Suggested stop': suggested_stop, "Beta": beta, "PE": pe} , ignore_index=True)

        elif row["SecType"] == "OPT":
            
            position = float(row["Position"])
            right = row["Right"]

            target_row = None
            if(position < 0):
                if right == "P":
                    target_row = sp_row
                elif right == "C":
                    target_row = sc_row
            elif (position > 0):
                if right == "P":
                    target_row = lp_row
                elif right == "C":
                    target_row = lc_row

            if target_row is not None:
                target_row["Total USD"] = target_row["Total USD"] + abs(total)
                target_row["Unrealized profit"] = target_row["Unrealized profit"] + unrealized_profit

    stock_total = stock_df['Total USD'].sum()
    if sp_row["Total USD"] > 0:
        stock_df = stock_df.append(sp_row, ignore_index=True)
    if sc_row["Total USD"] > 0:
        stock_df = stock_df.append(sc_row, ignore_index=True)
    if lp_row["Total USD"] > 0:
        stock_df = stock_df.append(lp_row, ignore_index=True)
    if lc_row["Total USD"] > 0:
        stock_df = stock_df.append(lc_row, ignore_index=True)

    for index, row  in stock_df.iterrows():
        #print("d", row["Total USD"], stock_total)
        row["Pct."] = float(row["Total USD"]) / float(stock_total)


    return stock_df

def __archive_data(config, stock_df, crypto_df):
    #purge data > 1 month
    #upload latest to cloud
    __remove_old_data(config["archive_location"], config["day_archive"])
    h5_name = "data" + datetime.today().strftime("%Y%m%d") + ".h5"
    h5_path = os.path.join(config["archive_location"], h5_name)

    stock_df.to_hdf(h5_path, key='stock')
    stock_df.to_hdf(h5_path, key='crypto')

    __sftp_data(h5_path, config)
    pass

def __remove_old_data(filesPath, archive_days):

    criticalTime = arrow.now().shift(days=-archive_days)

    for item in Path(filesPath).glob('*'):
        if item.is_file():
            itemTime = arrow.get(item.stat().st_mtime)
            if itemTime < criticalTime:
                os.remove(str(item.absolute()))

def __sftp_data(file_local_path, config):
    # Accept any host key (still wrong see below)
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None

    file_remote_dir = config["archive_sftp"]
    sftp = pysftp.Connection(config["synology_sftp_url"], port=config["synology_sftp_port"], username=config["synology_username"], password=config["synology_password"], private_key=".ppk",
    cnopts=cnopts)
    sftp.chdir(file_remote_dir)
    sftp.put(file_local_path)


def __commit_gitpage(report_location):
    '''Run command to commit report to my git page'''
    pass

def __generate_pie_chart(df):
    '''
    generate a string on the graph:
    https://stackoverflow.com/questions/5453375/matplotlib-svg-as-string-and-not-a-file
    '''
    fig, axs = plt.subplots(figsize=(8, 5)) 
    plot = df.plot.pie(y='Weighting', ax=axs, autopct='%1.1f%%')

    imgdata = StringIO()
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)  # rewind the data

    svg_dta = imgdata.read()  # this is svg data 
    print("debug svg: ", svg_dta)
    return svg_dta

def __generate_crypto_pie(portfolio):

    # create a new df 
    df = pd.DataFrame(columns = [
        "Symbol", "Weighting"
    ])

    for index, row in portfolio.iterrows():
        symbol = row["Symbol"]
        weight = row["Total USD"]
        df = df.append({"Symbol": symbol, "Weighting": weight}, ignore_index=True)

    print("Debug crypto: ",df)

    df.set_index('Symbol', inplace=True)
    
    return __generate_pie_chart(df)

def __generate_stock_pie(portfolio):
    '''
    generate a string on the graph:
    https://stackoverflow.com/questions/5453375/matplotlib-svg-as-string-and-not-a-file
    '''
    # create a new df 
    df = pd.DataFrame(columns = [
        "Symbol", "Weighting"
    ])

    for index, row in portfolio.iterrows():
        symbol = row["Symbol"]
        weight = row["Total USD"]
        df = df.append({"Symbol": symbol, "Weighting": weight}, ignore_index=True)

    df.set_index('Symbol', inplace=True)
    
    print("Debug crypto: ",df)

    return __generate_pie_chart(df)

def generate_report():
    
    config = __read_config()

    crypto = __get_crypto_data(config)
    stock_us = __get_stock_data_us(config)

    crypto_total = crypto['Total USD'].sum()
    stock_total = stock_us['Total USD'].sum()

    crypto_pie_svg = __generate_crypto_pie(crypto)
    stock_pie_svg = __generate_stock_pie(stock_us)
    
    # Then generate report
    current_date = datetime.today().date()
    title_text = "Asset report: " + current_date.strftime("%Y%m%d")
    report_name = "asset_" + current_date.strftime("%Y%m%d") + ".html"
    # 2. Combine them together using a long f-string
    html = f'''
        <html>
            <head>
                <title>{title_text}</title>
            </head>
            <body>
                <h1>{title_text}</h1>
                <h2>Stock information: </h2>
                {stock_us.to_html()}

                <h2>Weighting</h2>
                {stock_pie_svg}

                <p>Total assets in stock: {stock_total}</p>

                <h2>Cryto information</h2>
                {crypto.to_html()}

                <h2>Weighting</h2>
                {crypto_pie_svg}

                <p>Total assets in crypto: {crypto_total}</p>
            </body>
        </html>
        '''

    report_path = os.path.join(config["report_location"], report_name)

    with open(report_path, 'w') as f:
        f.write(html)
    
    __archive_data(config, stock_us, crypto)

if __name__ == '__main__':
    generate_report()

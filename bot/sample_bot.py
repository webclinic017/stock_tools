## Sample bot definition
import os

from datetime import datetime, timedelta, timezone
"""
I am trading multiple symbol

Filter
Only trade the top 10 hot? => It is a multiple symbol system and also available on ByBit

Do a simple SMA -> and then we can talk about GMMA

Divide it into _X_ bet and
Where there is Y bet already there, divide the money into X - Y bet and use it to trade

When the trade bot loss money to => $L (total account equity) liquidate all the position stop trading and send an email to me to say sorry.
"""

def getAssetCash():
    pass

def getCryptoCurrentPrice():
    pass

def getNoOfActivePosition():
    pass

def getFilterSymbol():
    pass

def getEnv(key, default_value=None):
    # check env have key
    if key in os.environ:
        return os.environ(key)
    else:
        return default_value

daily_refresh_time = getEnv("daily_refresh", "12:00")
max_symbol = os.getenv('max_symbol')
filter_symbol = getFilterSymbol()
stop_loss_limit = os.getenv('stop_loss_limit')
trade_interval = getEnv('trade_interval', 5)


current_active = getNoOfActivePosition()
#get yesterday
def getYesterday():
    today = datetime.today()
    yesterday = today - timedelta(days=1)
    return yesterday.strftime("%Y-%m-%d")

def getGreedAndFear():
    pass


daily_data_version =getYesterday()
greed_and_fear = 0


def updateDailyData():
    
    daily_data_version = datetime.today().strftime("%Y-%m-%d")

def trade():
    pass

def sendEmail():
    pass

def havePosition(symbol):
    return False

def openLongPosition(symbol):
    pass

def openShortPosition(symbol):
    pass

def closePosition(symbol):
    pass

def updateTicker(symbol):
    pass

class SimpleSMA():
    ## Can have a trade bot to determine 1d graph is up or down and trade accordingly?
    def __init__(self, symbol, interval, period):
        self.symbol = symbol

    def next():
        pass

def main():
    # parameter setup
    sma = SimpleSMA()

    # trade part
    while True:
        
        if(datetime.now().strftime("%H:%M") > daily_refresh_time and
             daily_data_version != datetime.today().strftime("%Y-%m-%d")):
            updateDailyData()

        asset_cash = getAssetCash()
        asset_crypto = getCryptoCurrentPrice()


        if(asset_cash + asset_crypto < stop_loss_limit):
            # TODO: liquidate all position
            # stop
            break

        trade_lot = asset_cash / (max_symbol - current_active)

        # Now for each symbol, see if we can trade
        for symbol in filter_symbol:
            # Get current price and update tickers
            updateTicker(symbol)

            # check if we can trade
            if(current_active < max_symbol and not havePosition(symbol)):
                # code the trading logic here
                action = sma.next()

                # Do I need to consider close and open reverse direction?
                if(action == 1):
                    openLongPosition()
                elif (action == 0):
                    closePosition()
                elif (action == -1):
                    openShortPosition()

            # sleep for a while and wait for next ticker update


if name == '__main__':
    main()
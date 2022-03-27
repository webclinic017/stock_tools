# Observer and analyzer
# Tom
# source: https://www.youtube.com/watch?v=FykJ4hAnV5o&list=PLHxM50fGnEoVSkh8PAI7dTWtEFJuu9Yom&index=15

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

# Writer and analyzer
# How to generate report look like the book in backtester
# Pyfolio: quantopian stop working, but still seems to work, and no one step up to get the main fork

# data feeds
import datetime
import backtrader as bt
import pandas as pd

class three_bars(bt.Indicator):
    # what are the lines?
    lines = ('up', 'down')

    def __init__(self):
        self.addminperiod(4)
        self.plotinfo.plotmaster = self.data

    def next(self):
        #self.lines[0] => resolve to up
        self.down[0] = min(min(self.data.close.get(ago=-1, size=3)), min(self.data.open.get(ago=-1, size=3)))
        self.up[0] = max(max(self.data.close.get(ago=-1, size=3)), max(self.data.open.get(ago=-1, size=3)))

class MyStrategy(bt.Strategy):
    def __init__(self):
        #print("init")
        self.up_down = three_bars(self.data)
        self.buy_signal = bt.indicators.CrossOver(self.data.close, self.up_down.up)
        self.sell_signal = bt.indicators.CrossOver(self.data.close, self.up_down.down)
        self.buy_signal.plotinfo.plot = False
        self.sell_signal.plotinfo.plot = False
        #self.up_down.plotinfo.plot = False


    def start(self):
        print("start")

    def prenext(self):
        print("prenext")

    def nextstart(self):
        print("nextstart")

    def next(self):
        #print("next")
        #ma_value = sum(self.data.close[-cnt] for cnt in range(0, 24)) / 24
        """ ma_value = self.bt_sma[0]
        pre_ma_value = self.bt_sma[-1]

        if self.data.close[0] > ma_value and self.data.close[-1] <= pre_ma_value:
            self.order = self.buy()

        if self.data.close[0] < ma_value and self.data.close[-1] >= pre_ma_value:
            self.order = self.sell() """

        if not self.position and self.buy_signal[0] == 1:
            self.order = self.buy()

        if not self.position and self.sell_signal[0] == 1:
            self.order = self.sell()

        if self.getposition().size < 0 and self.buy_signal[0] == 1:
            self.order =self.close()
            self.order =self.buy()

        if self.getposition().size > 0 and self.sell_signal[0] == 1:
            self.order = self.close()
            self.order = self.sell()

    def stop(self):
        print("stop")

# 初始化cerebro
#cerebro = bt.Cerebro()
cerebro = bt.Cerebro(stdstats=False)

# Add observer
cerebro.addobserver(bt.observers.Broker)
cerebro.addobserver(bt.observers.Trades)
cerebro.addobserver(bt.observers.BuySell)
cerebro.addobserver(bt.observers.DrawDown)
cerebro.addobserver(bt.observers.Value)
cerebro.addobserver(bt.observers.TimeReturn)

# feed data

# Create from panda data frame
dataframe = pd.read_csv("../data/TSLA.csv")
dataframe['Date'] = pd.to_datetime(dataframe['Date'])
dataframe.set_index('Date', inplace=True)
dataframe['openinterest'] = 0

brf_daily = bt.feeds.PandasData(dataname=dataframe, 
    #fromdate=datetime.datetime(2021,5,13), 
    #todate=datetime.datetime(2021,6,20), 
    datetime=None,
    high=1,
    low=2,
    open=0,
    close=4,
    volume=5,
    openinterest=6,)

cerebro.adddata(brf_daily)

# add strategy
cerebro.addstrategy(MyStrategy)


# add analyzer
cerebro.addanalyzer(bt.analyzers.SharpeRatio)
cerebro.addanalyzer(bt.analyzers.DrawDown)
cerebro.addanalyzer(bt.analyzers.TradeAnalyzer)
cerebro.addanalyzer(bt.analyzers.Transactions)

# pyfolio
cerebro.addanalyzer(bt.analyzers.PyFolio)
# cerebro.addwriter(bt.WriterFile, csv=True, out='backtest_result.csv')

# run backtest
res = cerebro.run()[0]

# print result
#print('Sharpe Ratio: ', res.analyzers.sharperatio.get_analysis())
#print('Drawdown: ', res.analyzers.drawdown.get_analysis())
#print('TradeAnalyzer: ', res.analyzers.tradeanalyzer.get_analysis())
#print('Transactions: ', res.analyzers.transactions.get_analysis())

trading_data = res.analyzers.tradeanalyzer.get_analysis()
print("=====")
print("===win===")
print("won ratio: %s" % (trading_data['won']['total'] / float(trading_data['won']['total'] + trading_data['lost']['total'])))
print("won hits: %s" % trading_data['won']['total'])
print("won pnl --> total: %s, average: %s, max: %s" %
    (
        trading_data['won']['pnl']['total'],
        trading_data['won']['pnl']['average'],
        trading_data['won']['pnl']['max']
    )
)

print("===lost===")
print("lost hits: %s" % trading_data['lost']['total'])
print("lost pnl --> total: %s, average: %s, max: %s" %
    (
        trading_data['lost']['pnl']['total'],
        trading_data['lost']['pnl']['average'],
        trading_data['lost']['pnl']['max']
    ))

# pyfolio store result
pyfolio = res.analyzers.getbyname('pyfolio')
returns, positions, transactions, gross_lev = pyfolio.get_pf_items()

print("debug returns: ", returns)

#returns.to_hdf('return.h5', key='data')
#positions.to_hdf('position.h5', key='data')
#transactions.to_hdf('transactions.h5', key='data')


# plot diagram
cerebro.plot(style='candlestick', barup='green', bardown='red')


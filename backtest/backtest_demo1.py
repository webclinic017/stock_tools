# Three bar - SMA(24) cross k-line
# Tom
# source: https://www.youtube.com/watch?v=WxZxVdjIE-A&list=PLHxM50fGnEoVSkh8PAI7dTWtEFJuu9Yom&index=6


from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
# don't know why on mac the plot have time component.
# seems the candlestick does not show ohlc in matplotlib.
# for trying backtrader

# data feeds
import datetime
import backtrader as bt
import pandas as pd

class MyStrategy(bt.Strategy):
    def __init__(self):
        #print("init")
        self.bt_sma = bt.indicators.MovingAverageSimple(self.data, period=24)
        self.buy_sell_signal = bt.indicators.CrossOver(self.data.close, self.bt_sma)
        
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

        if not self.position and self.buy_sell_signal[0] == 1:
            self.order = self.buy()

        if not self.position and self.buy_sell_signal[0] == -1:
            self.order = self.sell()

        if self.position and self.buy_sell_signal[0] == 1:
            self.order =self.close()
            self.order =self.buy()

        if self.position and self.buy_sell_signal[0] == -1:
            self.order = self.close()
            self.order = self.sell()

    def stop(self):
        print("stop")

# 初始化cerebro
cerebro = bt.Cerebro()
# feed data

# Create from panda data frame
dataframe = pd.read_csv("../data/TSLA.csv")
dataframe['Date'] = pd.to_datetime(dataframe['Date'])
dataframe.set_index('Date', inplace=True)
dataframe['openinterest'] = 0

brf_daily = bt.feeds.PandasData(dataname=dataframe, 
    fromdate=datetime.datetime(2021,5,13), 
    todate=datetime.datetime(2021,6,20), 
    datetime=None,
    high=1,
    low=2,
    open=0,
    close=4,
    volume=5,
    openinterest=6,)


#Create from a csv data feed
brf_daily = bt.feeds.GenericCSVData(dataname = "../data/TSLA.csv",
    nullvalue = 0.0,
    #fromdate=datetime.datetime(2021,5,13), 
    #todate=datetime.datetime(2021,6,20), 
    dtformat = ('%Y-%m-%d'),
    datetime = 0,
    high=2,
    low=3,
    open=1,
    close=5,
    volume=6,
    openinterest=None)


cerebro.adddata(brf_daily)

# add strategy
cerebro.addstrategy(MyStrategy)
# run backtest
cerebro.run()
# plot diagram
cerebro.plot(style='candlestick', barup='green', bardown='red')
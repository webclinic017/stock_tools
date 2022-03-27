# Introduce the concept of broker and slippage
# Tom
# source: https://www.youtube.com/watch?v=Y0JvnYz9W40&list=PLHxM50fGnEoVSkh8PAI7dTWtEFJuu9Yom&index=11

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
# don't know why on mac the plot have time component.
# seems the candlestick does not show ohlc in matplotlib.
# for trying wrting simple indicator

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

#What is the use of name?
cerebro.adddata(brf_daily, name='brf')

# add strategy
cerebro.addstrategy(MyStrategy)

# broker setting
cerebro.broker.setcash(20000.0)
# future mode
#cerebro.broker.setcommission(commission=2.0, margin=2000.0, mult=1.0, name='brf')
# stock mode
cerebro.broker.setcommission(commission=0.003, name='brf')
#slippage setting
#cerebro.broker.set_slippage_fixed(fixed=0.05)
cerebro.broker.set_slippage_perc(perc=0.0005)

#filler setting
cerebro.broker.set_filler(bt.broker.fillers.FixedBarPerc(perc=0.1))
#cerebro.broker.set_filler(bt.broker.fillers.FixedSize(size=1))

# run backtest
cerebro.run()
# plot diagram
cerebro.plot(style='candlestick', barup='green', bardown='red')
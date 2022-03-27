# Dual thrust
# Tom
# source: https://www.youtube.com/watch?v=7UYGAV0EvPE&list=PLHxM50fGnEoVSkh8PAI7dTWtEFJuu9Yom&index=7


from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
# don't know why on mac the plot have time component.
# Earning only a dollar or few cent, should control the sizing

# data feeds
import datetime
import backtrader as bt
import pandas as pd

class DT_Line(bt.Indicator):
    lines = ('U', 'D')
    params = (('period', 2), ('k_u', 0.7), ('k_d', 0.7))

    def __init__(self):
        self.addminperiod(self.p.period+1)

    def next(self):
        HH = max(self.data.high.get(-1, size=self.p.period))
        LC = min(self.data.close.get(-1, size=self.p.period))
        HC = max(self.data.close.get(-1, size=self.p.period))
        LL = min(self.data.low.get(-1, size=self.p.period))
        R = max(HH - LC, HC - LL)
        self.lines[0][0] = self.data.open[0] + self.p.k_u * R
        self.lines[1][0] = self.data.open[0] - self.p.k_d * R

class DualThrust(bt.Strategy):

    params = (('period', 2), ('k_u', 0.7), ('k_d', 0.7))

    def __init__(self):
        #self.data1.plotinfo.plot=False
        self.dataclose = self.data0.close
        self.D_Line = DT_Line(self.data1, period=self.p.period, k_u=self.p.k_u, k_d = self.p.k_d)

        self.D_Line = self.D_Line()
        #self.D_Line.plotinfo.plot = False
        self.D_Line.plotinfo.plotmaster=self.data0
  
        self.buy_signal = bt.indicators.CrossOver(self.dataclose, self.D_Line.U)
        # Error when the close cross above the dataclose.
        #self.sell_signal = bt.indicators.CrossOver(self.dataclose, self.D_Line.D)
        self.sell_signal = bt.indicators.CrossOver(self.D_Line.D, self.dataclose)

    def start(self):
        #print("start")
        pass

    def prenext(self):
        #print("prenext")
        pass

    def nextstart(self):
        #print("nextstart")
        pass

    def next(self):

        if self.data.datetime.time() >= datetime.time(9, 33) and self.datetime.time() < datetime.time(15, 55):

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

        if self.data.datetime.time() >= datetime.time(15, 55) and self.position:
            self.order = self.close()

    def stop(self):
        #print("stop")
        print("period: %s, k_u: %s, k_d: %s, final value: %.2f" % (self.p.period, self.p.k_u, self.p.k_d, self.broker.getvalue()))

if __name__ == '__main__':

    # 初始化cerebro
    cerebro = bt.Cerebro()
    # feed data

    #Create from a csv data feed
    brf_min_bar = bt.feeds.GenericCSVData(dataname = "../data/aapl_min.csv",
        nullvalue = 0.0,
        #fromdate=datetime.datetime(2021,5,13), 
        #todate=datetime.datetime(2021,6,20), 
        dtformat = ('%Y-%m-%d %H:%M:%S'),
        datetime = 0,
        high=2,
        low=3,
        open=4,
        close=1,
        volume=5,
        openinterest=None,
        timeframe=bt.TimeFrame.Minutes
        )

    cerebro.adddata(brf_min_bar)
    cerebro.resampledata(brf_min_bar, timeframe=bt.TimeFrame.Days)

    # add strategy
    #cerebro.addstrategy(DualThrust)
    cerebro.optstrategy(DualThrust,
        period=range(1, 5), k_u=[n/10.0 for n in range(2, 10)], k_d=[n/10.0 for n in range(2, 10)]
        )

    # run backtest
    cerebro.run()
    # plot diagram
    #cerebro.plot(style='candlestick', barup='green', bardown='red')
# How to use this?: use with email alert to tell you

import yfinance as yf
import datetime as dt
import panda as dt
from panda_datareader as pdf
import matplotlib.pyplot as plt

yf.pdr_override()
start = dt.datetime()
now = dt.datetime.now()

stock = input("Enter the stock symbol: ")

while stock != "quit":

    df = pdr.get_data_yahoo()
    df["High"].plot(label="high")

    pivots = []
    dates = []
    counter = 0
    lastPivot = 0

    Range = [0,0,0,0,0,0,0,0,0,0]
    dateRange = [0,0,0,0,0,0,0,0,0,0]

    for i in df.index
        currentMax = max(Range, default=0)
        value=round(df["High"][i], 2)

        Range = Range[1:9]
        Range.append(value)
        dateRange = dateRange[1:9]
        dateRange.append(i)

        if currentMax == max(Range, default=0)
            counter +=1
        else:
            counter = 0
        
        if counter == 5:
            lastPivot = currentMax
            dateloc = Range.index(lastPivot)
            lastDate = dateRange[dateloc]
            pivots.append(lastPivot)
            dates.append(lastDate)

    print()

    #print(str(pivots))
    #print(str(dates))
    timeD = dt.timedelta(days = 30)


    for index in range(len(pivots)):
        print(str(pivots[index]) +": " + str(dates[index]))

        plt.plot_data([dates[index], dates[index] + timeD], 
            [pivots[index], pivots[index]], linestyle="-", linewidth=2, marker="none")


    plt.show()


    stock = input("Enter the stock symbol: ")
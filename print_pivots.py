# Author: Om Prakash Manivannan
# Description: Pulls stock market data from Yahoo Finance and identifies Min/Max pivots
# Input: Update the "ticker_list" variable

import yfinance as yf
import datetime as dt
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt

yf.pdr_override()
start = dt.datetime(2019, 6, 1)
now = dt.datetime.now()

class stockTracker:
    def __init__(self, stock):
        self.stock = stock
        self.highPivots = []
        self.highDates = []
        self.lowPivots = []
        self.lowDates = []
        self.lowCounter = 0
        self.highCounter = 0
        self.lastHighPivot = 0
        self.HighRange = [0,0,0,0,0,0,0,0,0,0]
        self.dateHighRange = [0,0,0,0,0,0,0,0,0,0]
        self.lastLowPivot = 0
        self.LowRange = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.dateLowRange = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    def getStockData(self):
        return pdr.get_data_yahoo(self.stock, start, now)

    def findMinAndMax(self):
        df = self.getStockData()
        df["High"].plot(Label="high")
        df["Low"].plot(Label="low")
        for i in df.index:
            currentMax = max(self.HighRange, default=0)
            high_value = round(df["High"][i],2)
            self.HighRange=self.HighRange[1:9]
            self.HighRange.append(high_value)
            self.dateHighRange = self.dateHighRange[1:9]
            self.dateHighRange.append(i)
            if currentMax==max(self.HighRange, default=0):
                self.highCounter+=1
            else:
                self.highCounter = 0
            if self.highCounter == 5:
                lastHighPivot = currentMax
                datehighloc = self.HighRange.index(lastHighPivot)
                lastHighDate = self.dateHighRange[datehighloc]
                self.highPivots.append(lastHighPivot)
                self.highDates.append(lastHighDate)
            currentMin = min(self.LowRange, default=0)
            low_value = round(df["Low"][i],2)
            self.LowRange=self.LowRange[1:9]
            self.LowRange.append(low_value)
            self.dateLowRange = self.dateLowRange[1:9]
            self.dateLowRange.append(i)
            if currentMin==min(self.LowRange, default=0):
                self.lowCounter+=1
            else:
                self.lowCounter = 0
            if self.lowCounter == 5:
                lastLowPivot = currentMin
                datelowloc = self.LowRange.index(lastLowPivot)
                lastLowDate = self.dateLowRange[datelowloc]
                if lastLowPivot != 0:
                    self.lowPivots.append(lastLowPivot)
                    self.lowDates.append(lastLowDate)

        print("Low Pivots: ", self.lowPivots)
        print("High Pivots: ", self.highPivots)

    def getGreenLine(self):
        print("Green Line Values: " + self.stock)
        # TO DO

    def plotGraph(self):
        timeD = dt.timedelta(days=30)
        for low_index in range(len(self.lowPivots)):
            plt.plot_date([self.lowDates[low_index], self.lowDates[low_index] + timeD],
                          [self.lowPivots[low_index], self.lowPivots[low_index]], linestyle="-", linewidth=2, marker=",")
        for high_index in range(len(self.highPivots)):
            plt.plot_date([self.highDates[high_index], self.highDates[high_index]+timeD],
                          [self.highPivots[high_index], self.highPivots[high_index]], linestyle="dotted", linewidth=2, marker=",")

        plt.show()

ticker_list = ["TGT", "TSLA", "AAPL", "AMZN", "M", "DIS", "CMI"]

obj = {}
for tick in ticker_list:
    obj[tick] = stockTracker(tick)
    obj[tick].findMinAndMax()
    obj[tick].plotGraph()

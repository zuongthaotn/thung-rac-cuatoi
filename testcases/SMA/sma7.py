import warnings

warnings.filterwarnings('ignore')

import os
import sys
import pandas as pd

METHOD_MODULE_PATH = os.path.abspath('.')
sys.path.insert(1, METHOD_MODULE_PATH)
import vn_realtime_stock_data.stockHistory as stockHistory

ticker = 'POW'
htd = stockHistory.getAllStockHistoryData(ticker)  # not include today data
if 'Time' in htd.columns:
    from datetime import datetime

    htd['DateStr'] = htd.apply(
        lambda x: datetime.fromtimestamp(x['Time']).strftime("%Y-%m-%d"), axis=1)
htd['SMA_5'] = htd['Close'].rolling(window=5).mean()
htd['SMA_20'] = htd['Close'].rolling(window=20).mean()
htd['Date'] = pd.to_datetime(htd['DateStr'])
ticker_data = htd.set_index('Date')
ticker_data.drop(['Time'], axis=1)
ticker_data.drop(['DateStr'], axis=1)
ticker_data['Date'] = pd.to_datetime(ticker_data.index)

BACKTESTING_MODULE_PATH = os.path.abspath('backtest')
sys.path.insert(1, BACKTESTING_MODULE_PATH)
from backtesting.backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA

from math import atan2, degrees, cos
import math

def getAngle2(p1, p2, p3):
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    deg1 = (360 + degrees(atan2(x1 - x2, y1 - y2))) % 360
    deg2 = (360 + degrees(atan2(x3 - x2, y3 - y2))) % 360
    return deg2 - deg1 if deg1 <= deg2 else 360 - (deg1 - deg2)

def getAngle(p1, p2, p3):
    a = math.dist(p1, p2)
    b = math.dist(p2, p3)
    c = math.dist(p1, p3)
    print(a)
    print(b)
    print(c)
    return (a * a + b * b - c * c)/(2 * a * b)

class Sma07(Strategy):
    def init(self):
        price = self.data.Close
        self.buy_price = 0
        self.cross_price = 0
        self.sma_cross = 0
        self.ma5 = self.I(SMA, price, 5)
        self.ma20 = self.I(SMA, price, 20)

    def next(self):
        close_price = self.data.Close[-1]
        yesterday_close_price = self.data.Close[-2]
        last_sma5 = self.ma5[-1]
        last_sma20 = self.ma20[-1]
        if crossover(self.ma5, self.ma20):
            self.sma_cross = 1
            self.cross_price = last_sma5
        if self.buy_price == 0 and self.sma_cross == 1 and (last_sma5 - last_sma20) / yesterday_close_price > 0.06:
            self.buy()
            print(self.data.Date[-1])
            print(last_sma5)
            print(last_sma20)
            print(self.cross_price)
            print('---------------------------------------------------------------------------------------------')
            print(getAngle([0,last_sma20], [0, self.cross_price], [0, last_sma5]))
            print('---------------------------------------------------------------------------------------------')
            exit()
            self.buy_price = self.data.Close[-1]
        elif self.buy_price != 0 and (crossover(self.ma20, self.data.Close) or close_price < .99 * self.ma5[-1]):
            self.position.close()
            self.buy_price = 0

bt = Backtest(ticker_data, Sma07)
stats = bt.run()
# print(stats['_trades'])
# bt.plot()
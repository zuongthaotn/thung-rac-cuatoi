import warnings

warnings.filterwarnings('ignore')

import os
import sys
import pandas as pd
import numpy as np
import math

BACKTESTING_MODULE_PATH = os.path.abspath('backtest')
sys.path.insert(1, BACKTESTING_MODULE_PATH)
from backtesting.backtesting import Backtest, Strategy
from backtesting.test import SMA
from backtesting.lib import crossover
import method.SMA.v3 as v3
import method.algofuncs as _af

METHOD_MODULE_PATH = os.path.abspath('.')
sys.path.insert(1, METHOD_MODULE_PATH)
import vn_realtime_stock_data.stockHistory as stockHistory

ticker_id = 'MBB'
DATA_PATH = os.path.abspath('vn-stock-data/VNX/')
ticker_data = _af.get_pricing_by_path(DATA_PATH + '/' + ticker_id + '.csv', '2016-01-01', '2020-12-30')
prepared_data = v3.prepareDataVersionOffline(ticker_data)

class Sma01(Strategy):
    d = 0
    def init(self):
        self.buy_price = 0
        price = self.data.Close
        self.ma5 = self.I(SMA, price, 5)
        self.ma20 = self.I(SMA, price, 20)

    def next(self):
        try:
            if (len(self.data.SMA_H) < 21):
                return
            p1_sma_h = self.data.SMA_H[-1]
            p2_sma_h = self.data.SMA_H[-2]
            p3_sma_h = self.data.SMA_H[-3]
            close_price = self.data.Close[-1]
            open_price = self.data.Open[-1]
            self.d = self.d + 1
            # if p1_sma_h < 0:
            #     print(self.data.Date[-1])
            if self.buy_price == 0 and p1_sma_h > 0 and p2_sma_h > p1_sma_h and p3_sma_h > p2_sma_h and p3_sma_h / p1_sma_h > 2.5 :
            # if self.buy_price == 0 and p1_sma_h > 0 and p2_sma_h > p1_sma_h and p3_sma_h > p2_sma_h and p3_sma_h / p1_sma_h > 2.5 and close_price > open_price and close_price > self.ma5[-1] and open_price < self.ma20[-1]:
                self.buy()
                self.buy_price = close_price
                self.d = 0

            # elif self.buy_price != 0 and open_price > close_price and (close_price < self.data.SMA_5[-1] or p1_sma_h < 0) and self.d > 2:
            elif self.buy_price != 0 and (crossover(self.ma20, self.data.Close) or close_price < .99 * self.ma5[-1]) and self.d > 2:
            # elif self.buy_price != 0 and (crossover(self.ma20, self.data.Close) or close_price < .99 * self.ma5[-1] or self.data.Close[-2] < self.data.Open[-1] or close_price < open_price) and self.d > 2:
                self.position.close()
                self.buy_price = 0
        except:
            print("An exception occurred")

bt = Backtest(prepared_data, Sma01)
stats = bt.run()
print(stats)
# optimized_stats = bt.optimize(ma5=range(4, 7, 1), ma20=range(20, 30, 1))
# print(optimized_stats)
bt.plot()
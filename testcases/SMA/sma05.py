import warnings
warnings.filterwarnings('ignore')

import os
import sys

import method.algofuncs as _af

BACKTESTING_MODULE_PATH = os.path.abspath('backtest')
sys.path.insert(1, BACKTESTING_MODULE_PATH)
from backtesting.backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA

path = os.getcwd()

class Sma05(Strategy):
    def init(self):
        price = self.data.Close
        self.buy_price = 0
        self.ma5 = self.I(SMA, price, 5)
        self.ma20 = self.I(SMA, price, 20)

    def next(self):
        if self.buy_price == 0 and crossover(self.ma5, self.ma20):
            self.buy()
            self.buy_price = self.data.Close[-1]
        elif self.buy_price != 0 and crossover(self.ma20, self.data.Close):
            self.position.close()
            self.buy_price = 0


DATA_PATH = os.path.abspath('vn-stock-data/VNX/')
ticker_id = 'POW'
ticker_data = _af.get_pricing_by_path(DATA_PATH + '/' + ticker_id + '.csv', '2016-01-01', '2020-12-30')
# print(ticker_data)
# exit()
bt = Backtest(ticker_data, Sma05, commission=.005, exclusive_orders=False)
stats = bt.run()
bt.plot()

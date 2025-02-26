import warnings
warnings.filterwarnings('ignore')

import os
import sys
import pandas as pd

BACKTESTING_MODULE_PATH = os.path.abspath('../../backtest')
sys.path.insert(1, BACKTESTING_MODULE_PATH)
from backtesting.backtesting import Backtest, Strategy

METHOD_MODULE_PATH = os.path.abspath('../..')
sys.path.insert(1, METHOD_MODULE_PATH)
import method.Ticker as Ticker
import method.SaleRules as _sr
import method.algofuncs as _af

path = os.getcwd()
STOPLOSS = 0.08
class FollowTheTrend(Strategy):
    def init(self):
        self.buy_price = 0
        self.trailing_price = 0
    def next(self):
        prices = self.data.Close
        opens = self.data.Open
        volumes = self.data.Volume
        if len(self.data.Volume) > 5:
            last_price = prices[-1]
            # price is increased
            if last_price > self.trailing_price:
                self.trailing_price = last_price

            if self.buy_price == 0 and Ticker.isFollowTrendingV2(prices, volumes, opens[-1], 2.5):
                self.buy_price = last_price
                self.buy()
            if self.buy_price != 0:
                if _sr.takeProfitByPercent(15, last_price, self.buy_price) or last_price < self.buy_price * (1 - STOPLOSS) or last_price < self.trailing_price * (1 - STOPLOSS):
                    self.position.close()
                    self.buy_price = 0
                    self.trailing_price = 0

ticker_id = 'HBC'
DATA_PATH = os.path.abspath('../../vn-stock-data/VNX/')
ticker = _af.get_pricing_by_path(DATA_PATH + '/' + ticker_id+'.csv', '2010-01-01', '2020-10-05')
bt = Backtest(ticker, FollowTheTrend, commission=.005, exclusive_orders=False)
stats = bt.run()
# bt.plot()
print(stats)
# print(stats['_trades'])
# new_file = path+"/result_"+ticker_id+".csv"
# stats['_trades'].to_csv(new_file, index=False)

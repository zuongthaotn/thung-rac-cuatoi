import warnings
warnings.filterwarnings('ignore')

import os
import sys
import numpy as np

BACKTESTING_MODULE_PATH = os.path.abspath('../../backtest')
sys.path.insert(1, BACKTESTING_MODULE_PATH)
from backtesting.backtesting import Backtest, Strategy

METHOD_MODULE_PATH = os.path.abspath('../..')
sys.path.insert(1, METHOD_MODULE_PATH)
import method.Ticker as Ticker
import method.SaleRules as _sr
import method.algofuncs as _af
path = os.getcwd()

DATA_PATH = os.path.abspath('../../vn-stock-data/VNX/')
ticker_id = 'TCH'
ticker_data = _af.get_pricing_by_path(DATA_PATH + '/' + ticker_id+'.csv', '2018-01-01')
ticker_data['avgHL'] = ticker_data.apply(lambda row: (row.High + row.Low) / 2, axis=1)

class StockBreakOut(Strategy):
    def init(self):
        self.buy_price = 0
        self._index = 0
    def next(self):
        prices = self.data.avgHL
        if len(self.data.Volume) > 22:
            last_price = prices[-1]
            if self.buy_price == 0 and Ticker.isCounterTrendV2(prices):
                self.buy_price = last_price
                self.buy()
            if self.buy_price != 0 and (_sr.takeProfitByPercent(5, last_price, self.buy_price) or _sr.shouldCutLossByPercent(8, last_price, self.buy_price)):
                self.position.close()
                self.buy_price = 0

bt = Backtest(ticker_data, StockBreakOut, commission=.005, exclusive_orders=False)
stats = bt.run()
print(stats)
bt.plot()
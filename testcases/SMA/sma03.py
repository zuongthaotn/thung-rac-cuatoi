import warnings
warnings.filterwarnings('ignore')

import os
import sys
BACKTESTING_MODULE_PATH = os.path.abspath('../../backtest')
sys.path.insert(1, BACKTESTING_MODULE_PATH)

METHOD_MODULE_PATH = os.path.abspath('../..')
sys.path.insert(1, METHOD_MODULE_PATH)
from backtesting.backtesting import Backtest, Strategy
from backtesting.test import SMA
from backtesting.lib import crossover
import method.algofuncs as _af
path = os.getcwd()

class SmaCross(Strategy):
    def init(self):
        price = self.data.Close
        self.buy_price = 0
        self.ma1 = self.I(SMA, price, 5)
        self.ma2 = self.I(SMA, price, 10)

    def next(self):
        if self.buy_price == 0 and crossover(self.ma1, self.ma2):
            self.buy()
            self.buy_price = self.data.Close[-1]
        elif self.buy_price != 0 and crossover(self.ma2, self.ma1):
            self.position.close()
            self.buy_price = 0


ticker_id = 'PNJ'
DATA_PATH = os.path.abspath('../../vn-stock-data/VNX/')
ticker = _af.get_pricing_by_path(DATA_PATH + '/' + ticker_id+'.csv', '2017-01-01', '2020-10-05')
bt = Backtest(ticker, SmaCross, commission=.005, exclusive_orders=False)
stats = bt.run()
bt.plot()
print(stats)

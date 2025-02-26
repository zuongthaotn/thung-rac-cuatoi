import warnings

warnings.filterwarnings('ignore')

import os
import sys

import method.algofuncs as _af
import method.JavCan as jModel

BACKTESTING_MODULE_PATH = os.path.abspath('backtest')
sys.path.insert(1, BACKTESTING_MODULE_PATH)
from backtesting.backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA

path = os.getcwd()


class SmaCross(Strategy):
    def init(self):
        self.orderPending = False
        price = self.data.Close
        self.ma1 = self.I(SMA, price, 5)
        self.ma2 = self.I(SMA, price, 20)
        # self.ma3 = self.I(SMA, price, 1)

    def next(self):
        if crossover(self.ma1, self.ma2) and self.orderPending is False:
            self.buy()
            self.orderPending = True

        if crossover(self.ma2, self.ma1) and self.orderPending is True:
            self.position.close()
            self.orderPending = False

DATA_PATH = os.path.abspath('vn-stock-data/VNX/')
ticker_id = 'ACB'
# ticker_data = _af.get_pricing_by_path(DATA_PATH + '/' + ticker_id + '.csv', '2020-01-01')
ticker_data = _af.get_pricing_by_path(DATA_PATH + '/' + ticker_id + '.csv', '2016-01-01', '2020-12-30')
new_data = jModel.convertToJapanCandle(ticker_data)
bt = Backtest(ticker_data, SmaCross, commission=.005, exclusive_orders=False)
stats = bt.run()
bt.plot()


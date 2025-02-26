import warnings

warnings.filterwarnings('ignore')

import pandas as pd
import numpy as np


def SMA(array, n):
    """Simple moving average"""
    return pd.Series(array).rolling(n).mean()


import os
import sys

METHOD_MODULE_PATH = os.path.abspath('../..')
sys.path.insert(1, METHOD_MODULE_PATH)
import method.algofuncs as _af
import method.JavCan as jModel

BACKTESTING_MODULE_PATH = os.path.abspath('../../backtest')
sys.path.insert(1, BACKTESTING_MODULE_PATH)
from backtesting.backtesting import Backtest, Strategy
from backtesting.lib import crossover

path = os.getcwd()

LOOK_BACK = 6


class Test06(Strategy):
    d_sma = 5

    def init(self):
        self.orderPending = False
        moment = self.data.Moment
        self.ma1 = self.I(SMA, moment, self.d_sma)

    def next(self):
        zero_l = self.data.Zero
        if crossover(self.ma1, zero_l) and self.orderPending is False:
            self.buy()
            self.orderPending = True

        if crossover(zero_l, self.ma1) and self.orderPending is True:
            self.position.close()
            self.orderPending = False



DATA_PATH = os.path.abspath('../../vn-stock-data/VNX/')
ticker_id = 'VCB'
ticker_data = _af.get_pricing_by_path(DATA_PATH + '/' + ticker_id + '.csv', '2018-01-01')
new_data = jModel.convertToJapanCandle(ticker_data)
new_data['Moment'] = new_data.apply(lambda x: (x['Body'] - x['UpShadow'] - x['LowerShadow']) / x['Height'], axis=1)
new_data['Zero'] = new_data.apply(lambda x: 0, axis=1)
bt = Backtest(ticker_data, Test06, commission=.005, exclusive_orders=False)
stats = bt.run()
optimized_stats = bt.optimize(d_sma=range(1, 15, 1))
print(optimized_stats)
bt.plot()

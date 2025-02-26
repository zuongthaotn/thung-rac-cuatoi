import warnings

warnings.filterwarnings('ignore')

import os
import sys

import method.algofuncs as _af
import method.JavCan as jModel

BACKTESTING_MODULE_PATH = os.path.abspath('backtest')
sys.path.append(BACKTESTING_MODULE_PATH)
from backtesting import Backtest, Strategy


path = os.getcwd()

import pandas as pd
import numpy as np


def SMA(array, n):
    """Simple moving average"""
    return pd.Series(array).rolling(n).mean()

LOOK_BACK = 6


class Test07(Strategy):
    d_sma = 3

    def init(self):
        self.orderPending = False
        moment = self.data.Moment
        self.ma1 = self.I(SMA, moment, self.d_sma)

    def next(self):
        if self.orderPending is True:
            self.buy()
        # zero_l = self.data.Zero
        # if crossover(self.ma1, zero_l) and self.orderPending is False:
        #     self.buy()
        #     self.orderPending = True
        #
        # if crossover(zero_l, self.ma1) and self.orderPending is True:
        #     self.position.close()
        #     self.orderPending = False


def getMoment(_open, _close, _high, _low, _type):
    if _type == 1:
        if _open - _low != 0:
            return (_high - _close)/(_open - _low)
        else:
            return (_high - _close)/0.001

    if _type == 2:
        if _close - _low != 0:
            return (_open - _high) / (_close - _low)
        else:
            return (_open - _high) / 0.001



DATA_PATH = os.path.abspath('vn-stock-data/VNX/')
ticker_id = 'VCB'
ticker_data = _af.get_pricing_by_path(DATA_PATH + '/' + ticker_id + '.csv', '2018-05-01', '2018-05-30')
ticker_data['Moment'] = ticker_data.apply(
        lambda x: getMoment(x['Open'], x['Close'], x['High'], x['Low'], 1) if (x['Close'] > x['Open']) else getMoment(x['Open'], x['Close'], x['High'], x['Low'], 2), axis=1)
ticker_data['Zero'] = ticker_data.apply(lambda x: 0, axis=1)
print(ticker_data)
bt = Backtest(ticker_data, Test07, commission=.005, exclusive_orders=False)
stats = bt.run()
bt.plot()

import warnings
warnings.filterwarnings('ignore')

import numpy as np
import os
import sys
METHOD_MODULE_PATH = os.path.abspath('../..')
sys.path.insert(1, METHOD_MODULE_PATH)
import method.algofuncs as _af
import method.JavCan as jModel

BACKTESTING_MODULE_PATH = os.path.abspath('../../backtest')
sys.path.insert(1, BACKTESTING_MODULE_PATH)
from backtesting.backtesting import Backtest, Strategy

path = os.getcwd()

LOOK_BACK = 6

class ShavenBottomAndHead(Strategy):
    def init(self):
        self.orderPending = False
        self.orderIndex = 0

    def next(self):
        if len(self.data.Volume) > LOOK_BACK:
            prices = self.data.Close
            # if np.datetime64(self.data.Date[-1]) == np.datetime64('2020-04-03T00:00:00.000000000'):
            #     print('yesterday - isShavenBottom - ' + str(jModel.isShavenBottom(self.data.Height[-2], self.data.LowerShadow[-2])))
            #     print('today - isShavenHead - ' + str(jModel.isShavenHead(self.data.Height[-1], self.data.UpShadow[-1])))
            #     print('today - isWhiteCandlestick - ' + str(jModel.isWhiteCandlestick(self.data.Open[-1], self.data.Close[-1])))
            #     exit()

            hasBuySignal = jModel.hasCustomBuySignal(self.data.Open, self.data.Close, self.data.High, self.data.Low,
                                                     self.data.Body, self.data.Height, self.data.UpShadow,
                                                     self.data.LowerShadow, 3)

            if hasBuySignal is not False:
                self.buy(sl=0.9 * prices[-1], tp=1.2 * prices[-1])

DATA_PATH = os.path.abspath('../../vn-stock-data/VNX/')
ticker_id = 'OCB'
ticker_data = _af.get_pricing_by_path(DATA_PATH + '/' + ticker_id + '.csv', '2018-01-01')
new_data = jModel.convertToJapanCandle(ticker_data)
bt = Backtest(ticker_data, ShavenBottomAndHead, commission=.005, exclusive_orders=False)
stats = bt.run()
# print(stats)
# print(stats['_trades'])
bt.plot()
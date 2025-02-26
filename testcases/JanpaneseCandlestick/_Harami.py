import warnings
warnings.filterwarnings('ignore')

import os
import sys
import numpy as np

METHOD_MODULE_PATH = os.path.abspath('../..')
sys.path.insert(1, METHOD_MODULE_PATH)
import method.algofuncs as _af
import method.JavCan as jModel

BACKTESTING_MODULE_PATH = os.path.abspath('../../backtest')
sys.path.insert(1, BACKTESTING_MODULE_PATH)
from backtesting.backtesting import Backtest, Strategy

path = os.getcwd()

LOOK_BACK = 6


class Harami(Strategy):
    orderPending: bool

    def init(self):
        self.orderPending = False

    def next(self):
        if len(self.data.Volume) > LOOK_BACK:
            hasBuySignal = jModel.isBullishHarami(self.data.Open, self.data.Close, self.data.High, self.data.Low,
                                            self.data.Body, self.data.Height, self.data.UpShadow,
                                            self.data.LowerShadow)
            hasSellSignal = jModel.isBearishHarami(self.data.Open, self.data.Close, self.data.High, self.data.Low,
                                                 self.data.Body, self.data.Height, self.data.UpShadow,
                                                 self.data.LowerShadow)

            # if np.datetime64(self.data.Date[-1]) == np.datetime64('2018-07-12T00:00:00.000000000'):
            #     t4 = jModel.isMorningStarsPattern(self.data.Open, self.data.Close, self.data.High, self.data.Low, self.data.Body, self.data.Height, self.data.UpShadow, self.data.LowerShadow)
            #     print('today - isMorningStarsPattern - ' + str(t4))
            #     print(jModel.isBlackCandlestick(self.data.Open[-3], self.data.Close[-3]))
            #     print(jModel.isBodyOver45(self.data.Body[-3], self.data.Height[-3]))
            #     print(jModel.isBodyLess35(self.data.Body[-2], self.data.Height[-2]))
            #     print(jModel.isWhiteCandlestick(self.data.Open[-1], self.data.Close[-1]))
            #     exit()

            if hasBuySignal is not False and self.orderPending is False:
                self.buy()
                self.orderPending = True

            if hasSellSignal is not False and self.orderPending is True:
                self.position.close()
                self.orderPending = False


DATA_PATH = os.path.abspath('../../vn-stock-data/VNX/')
ticker_id = 'VRE'
ticker_data = _af.get_pricing_by_path(DATA_PATH + '/' + ticker_id + '.csv', '2018-01-01')
new_data = jModel.convertToJapanCandle(ticker_data)
bt = Backtest(ticker_data, Harami, commission=.005, exclusive_orders=False)
stats = bt.run()
print(stats)
# print(stats['_trades'])
bt.plot()

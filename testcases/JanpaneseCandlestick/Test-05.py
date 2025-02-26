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

class JavAllCustomWays(Strategy):
    def init(self):
        self.orderPending = False
        self.orderIndex = 0

    def next(self):
        if len(self.data.Volume) > LOOK_BACK:
            prices = self.data.Close
            hasBuySignal = jModel.hasCustomBuySignal(self.data.Open, self.data.Close, self.data.High, self.data.Low,
                                                    self.data.Body, self.data.Height, self.data.UpShadow,
                                                    self.data.LowerShadow)
            hasSellSignal = jModel.hasCustomSellSignal(self.data.Open, self.data.Close, self.data.High, self.data.Low,
                                                      self.data.Body, self.data.Height, self.data.UpShadow,
                                                      self.data.LowerShadow)
            # if np.datetime64(self.data.Date[-1]) == np.datetime64('2018-01-29T00:00:00.000000000'):
            #     t4 = jModel.isBearishEngulfing(self.data.Open, self.data.Close, self.data.High, self.data.Low, self.data.Body, self.data.Height, self.data.UpShadow, self.data.LowerShadow)
            #     print('today - isBearishEngulfing - ' + str(t4))
            #     exit()

            if hasBuySignal is not False and self.orderPending is False:
                self.buy()
                self.orderIndex = self.orderIndex + 1
                print(str(self.orderIndex) + ". Buy at " + str(self.data.Date[-1]) + " by signal: " + str(hasBuySignal))
                self.orderPending = True

            if hasSellSignal is not False and self.orderPending is True:
                self.position.close()
                print("----------- Sell at " + str(self.data.Date[-1]) + " by signal: " + str(hasSellSignal))
                self.orderPending = False

DATA_PATH = os.path.abspath('../../vn-stock-data/VNX/')
ticker_id = 'VHM'
ticker_data = _af.get_pricing_by_path(DATA_PATH + '/' + ticker_id + '.csv', '2018-01-01')
new_data = jModel.convertToJapanCandle(ticker_data)
bt = Backtest(ticker_data, JavAllCustomWays, commission=.005, exclusive_orders=False)
stats = bt.run()
# print(stats)
# print(stats['_trades'])
bt.plot()
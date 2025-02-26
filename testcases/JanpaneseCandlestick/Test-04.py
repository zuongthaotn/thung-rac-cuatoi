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

LOOK_BACK = 10

class JavAllWays(Strategy):
    def init(self):
        self.orderPending = False
        self.orderIndex = 0
        self.daily_rsi = self.I(_af.RSI, self.data.Close, 5)

    def next(self):
        if len(self.data.Volume) > LOOK_BACK:
            prices = self.data.Close
            hasBuySignal = jModel.hasBuySignal(self.data.Open, self.data.Close, self.data.High, self.data.Low,
                                                    self.data.Body, self.data.Height, self.data.UpShadow,
                                                    self.data.LowerShadow, self.data.Volume, self.data.Date)
            hasSellSignal = jModel.hasSellSignal(self.data.Open, self.data.Close, self.data.High, self.data.Low,
                                                      self.data.Body, self.data.Height, self.data.UpShadow,
                                                      self.data.LowerShadow, self.data.Volume, self.data.Date)
            # if np.datetime64(self.data.Date[-1]) == np.datetime64('2021-01-29T00:00:00.000000000'):
            #     t4 = jModel.isBullishEngulfing(self.data.Open, self.data.Close, self.data.High, self.data.Low, self.data.Body, self.data.Height, self.data.UpShadow, self.data.LowerShadow)
            #     print('today - isBullishEngulfing - ' + str(t4))
            #     print('today - isDoji - ' + str(jModel.isDoji(self.data.Body[-2], self.data.Height[-2])))
            #     print('today - isWhiteCandlestick - ' + str(jModel.isWhiteCandlestick(self.data.Open[-1], self.data.Close[-1])))
            #     print('today - isDownTrendV1 - ' + str(jModel.isDownTrendV1(self.data.Open, self.data.Close, self.data.High, self.data.Low, self.data.Body, self.data.Height, self.data.UpShadow, self.data.LowerShadow)))
            #     exit()

            if hasBuySignal is not False and self.orderPending is False:
                self.buy()
                self.orderIndex = self.orderIndex + 1
                print(str(self.orderIndex) + ". Buy at " + str(self.data.Date[-1]) + " by signal: " + hasBuySignal)
                self.orderPending = True

            if hasSellSignal is not False and self.orderPending is True:
                self.position.close()
                print("----------- Sell at " + str(self.data.Date[-1]) + " by signal: " + hasSellSignal)
                self.orderPending = False

DATA_PATH = os.path.abspath('../../vn-stock-data/VNX/')
ticker_id = 'VRE'
ticker_data = _af.get_pricing_by_path(DATA_PATH + '/' + ticker_id + '.csv', '2018-01-01')
new_data = jModel.convertToJapanCandle(ticker_data)
bt = Backtest(ticker_data, JavAllWays, commission=.005, exclusive_orders=False)
stats = bt.run()
# print(stats)
# print(stats['_trades'])
bt.plot()
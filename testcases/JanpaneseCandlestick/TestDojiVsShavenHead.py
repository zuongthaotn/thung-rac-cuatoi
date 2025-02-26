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

class DojiAndShavenHead(Strategy):
    def init(self):
        self.orderPending = False
        self.orderIndex = 0

    def next(self):
        if len(self.data.Volume) > LOOK_BACK:
            prices = self.data.Close
            # if np.datetime64(self.data.Date[-1]) == np.datetime64('2018-01-29T00:00:00.000000000'):
            #     t4 = jModel.isBearishEngulfing(self.data.Open, self.data.Close, self.data.High, self.data.Low, self.data.Body, self.data.Height, self.data.UpShadow, self.data.LowerShadow)
            #     print('today - isBearishEngulfing - ' + str(t4))
            #     exit()

            the1stDayIsBlack = jModel.isBlackCandlestick(self.data.Open[-3], self.data.Close[-3])
            isDownTrend = jModel.isDownTrendV1(self.data.Open, self.data.Close, self.data.High, self.data.Low, self.data.Body, self.data.Height, self.data.UpShadow, self.data.LowerShadow)
            the2ndDayIsDoji = jModel.isDoji(self.data.Body[-2], self.data.Height[-2])
            todayIsShavenHead = jModel.isShavenHead(self.data.Height[-1], self.data.UpShadow[-1])
            todayIsWhite = jModel.isWhiteCandlestick(self.data.Open[-1], self.data.Close[-1])

            if isDownTrend is True and the2ndDayIsDoji is True and todayIsShavenHead is True and todayIsWhite is True:
                hasBuySignal = True
            else:
                hasBuySignal = False

            if hasBuySignal is not False:
                self.buy(sl=0.9 * prices[-1], tp=1.2 * prices[-1])

DATA_PATH = os.path.abspath('../../vn-stock-data/VNX/')
ticker_id = 'VHM'
ticker_data = _af.get_pricing_by_path(DATA_PATH + '/' + ticker_id + '.csv', '2018-01-01')
new_data = jModel.convertToJapanCandle(ticker_data)
bt = Backtest(ticker_data, DojiAndShavenHead, commission=.005, exclusive_orders=False)
stats = bt.run()
# print(stats)
# print(stats['_trades'])
bt.plot()
import warnings
warnings.filterwarnings('ignore')

import os
import sys
METHOD_MODULE_PATH = os.path.abspath('../..')
sys.path.insert(1, METHOD_MODULE_PATH)
import method.algofuncs as _af
import method.JavCan as jModel

BACKTESTING_MODULE_PATH = os.path.abspath('backtest')
sys.path.insert(1, BACKTESTING_MODULE_PATH)
from backtesting.backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA

path = os.getcwd()

LOOK_BACK = 6

class Doji(Strategy):
    def init(self):
        self.orderPending = False
        price = self.data.Close
        self.ma1 = self.I(SMA, price, 5)
        self.ma2 = self.I(SMA, price, 20)
        # self.ma3 = self.I(SMA, price, 1)

    def next(self):
        if len(self.data.Volume) > LOOK_BACK:
            prices = self.data.Close

            isDownTrend = jModel.isDownTrendV1(self.data.Open, self.data.Close, self.data.High, self.data.Low, self.data.Body, self.data.Height, self.data.UpShadow, self.data.LowerShadow)
            todayIsDoji = jModel.isDoji(self.data.Body[-1], self.data.Height[-1])

            # if isDownTrend is True and todayIsDoji is True:
            #     self.orderPending = True
            #     self.buy()

            if crossover(self.ma1, self.ma2) and self.orderPending is False:
                self.buy()
                self.orderPending = True

            hasSellSignal = jModel.hasSellSignal(self.data.Open, self.data.Close, self.data.High, self.data.Low,
                                                 self.data.Body, self.data.Height, self.data.UpShadow,
                                                 self.data.LowerShadow, self.data.Volume, self.data.Date)
            # if hasSellSignal is not False and self.orderPending is True:
            #     self.position.close()
            #     self.orderPending = False

            if crossover(self.ma2, self.ma1) and self.orderPending is True:
                self.position.close()
                self.orderPending = False

            # todayIsBlack = jModel.isBlackCandlestick(self.data.Open[-1], self.data.Close[-1])
            # yesterdayIsBlack = jModel.isBlackCandlestick(self.data.Open[-2], self.data.Close[-2])
            # if todayIsBlack is True and yesterdayIsBlack is True and self.orderPending is True:
            #     self.position.close()
            #     self.orderPending = False


DATA_PATH = os.path.abspath('vn-stock-data/VNX/')
ticker_id = 'POW'
ticker_data = _af.get_pricing_by_path(DATA_PATH + '/' + ticker_id + '.csv', '2016-01-01', '2020-12-30')
new_data = jModel.convertToJapanCandle(ticker_data)
bt = Backtest(ticker_data, Doji, commission=.005, exclusive_orders=False)
stats = bt.run()
# print(stats)
# print(stats['_trades'])
bt.plot()
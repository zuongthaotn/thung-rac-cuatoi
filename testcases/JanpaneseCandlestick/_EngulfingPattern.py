import warnings
warnings.filterwarnings('ignore')

import os
import sys

import method.algofuncs as _af
import method.JavCan as jModel

BACKTESTING_MODULE_PATH = os.path.abspath('backtest')
sys.path.insert(1, BACKTESTING_MODULE_PATH)
from backtesting.backtesting import Backtest, Strategy

path = os.getcwd()

LOOK_BACK = 6


class Engulfing(Strategy):
    orderPending: bool

    def init(self):
        self.orderPending = False

    def next(self):
        if len(self.data.Volume) > LOOK_BACK:
            hasBuySignal = jModel.isBullishEngulfing(self.data.Open, self.data.Close, self.data.High, self.data.Low,
                                            self.data.Body, self.data.Height, self.data.UpShadow,
                                            self.data.LowerShadow)
            hasSellSignal = jModel.isBearishEngulfing(self.data.Open, self.data.Close, self.data.High, self.data.Low,
                                                 self.data.Body, self.data.Height, self.data.UpShadow,
                                                 self.data.LowerShadow)

            if hasBuySignal is not False and self.orderPending is False:
                self.buy()
                self.orderPending = True

            if hasSellSignal is not False and self.orderPending is True:
                self.position.close()
                self.orderPending = False


DATA_PATH = os.path.abspath('vn-stock-data/VNX/')
ticker_id = 'VRE'
ticker_data = _af.get_pricing_by_path(DATA_PATH + '/' + ticker_id + '.csv', '2018-01-01')
new_data = jModel.convertToJapanCandle(ticker_data)
bt = Backtest(ticker_data, Engulfing, commission=.005, exclusive_orders=False)
stats = bt.run()
print(stats)
# print(stats['_trades'])
bt.plot()

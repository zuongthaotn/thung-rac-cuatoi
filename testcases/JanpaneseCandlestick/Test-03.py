import warnings
warnings.filterwarnings('ignore')

import datetime
import numpy
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


class Test(Strategy):
    def init(self):
        self.buy_price = 0
        self._index = 0

    def next(self):
        if len(self.data.Volume) > 4:
            prices = self.data.Close
            opens = self.data.Open
            bodies = self.data.Body
            ups = self.data.UpShadow
            lows = self.data.LowerShadow
            height = self.data.Height
            dates = self.data.Date

            prevDayIsSpinningTopCandlestick = jModel.isSpinningTopCandlestick(bodies[-2], height[-2], ups[-2], lows[-2])
            prevDayIsBlackCandlestick = jModel.isBlackCandlestick(opens[-2], prices[-2])
            prevDayIsWhiteCandlestick = jModel.isWhiteCandlestick(opens[-2], prices[-2])
            prevDayMaxOpenClose = opens[-2] if opens[-2] > prices[-2] else prices[-2]
            prevDayMinOpenClose = opens[-2] if opens[-2] < prices[-2] else prices[-2]

            todayIsWhiteCandlestick = jModel.isWhiteCandlestick(opens[-1], prices[-1])
            todayIsBlackCandlestick = jModel.isBlackCandlestick(opens[-1], prices[-1])
            todayMaxOpenClose = opens[-1] if opens[-1] > prices[-1] else prices[-1]
            todayMinOpenClose = opens[-1] if opens[-1] < prices[-1] else prices[-1]

            if prevDayIsBlackCandlestick is True \
                    and prices[-1] >= opens[-2] \
                    and opens[-1] <= prices[-2] \
                    and todayIsWhiteCandlestick is True:
                # self.buy(sl=0.9*prices[-1], tp=1.2 * prices[-1])
                self.buy(sl=0.9 * prices[-1])

            if prevDayIsWhiteCandlestick is True \
                    and prices[-1] <= opens[-2] \
                    and opens[-1] >= prices[-2] \
                    and todayIsBlackCandlestick is True:
                self.position.close()

            if prevDayIsBlackCandlestick is True \
                    and ((prices[-1] <= opens[-2] and opens[-1] <= prices[-2] and todayIsBlackCandlestick is True) \
                            or prevDayMinOpenClose > todayMaxOpenClose):
                self.position.close()


DATA_PATH = os.path.abspath('../../vn-stock-data/VNX/')
ticker_id = 'FPT'
ticker_data = _af.get_pricing_by_path(DATA_PATH + '/' + ticker_id + '.csv', '2018-01-01')
new_data = jModel.convertToJapanCandle(ticker_data)
bt = Backtest(ticker_data, Test, commission=.005, exclusive_orders=False)
stats = bt.run()
print(stats)
# print(stats['_trades'])
bt.plot()
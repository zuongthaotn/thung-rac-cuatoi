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
            current_date = numpy.datetime_as_string(dates[-1], unit="D")

            isUmbrellaCandlestick = jModel.isUmbrellaCandlestick(bodies[-2], height[-2], ups[-2], lows[-2])
            isWhiteCandlestick = jModel.isWhiteCandlestick(opens[-1], prices[-1])
            isBlackCandlestick = jModel.isBlackCandlestick(opens[-1], prices[-1])
            isShavenHead = jModel.isShavenHead(height[-1], ups[-1])
            if isUmbrellaCandlestick is True and isWhiteCandlestick is True and prices[-1] > prices[-2] and isShavenHead is True:
                self.buy(sl=0.9*prices[-1], tp=1.2 * prices[-1])
                # self.buy(sl=0.9*prices[-1])
            # if isUmbrellaCandlestick is True and isBlackCandlestick is True:
            #     self.position.close()

            py_date = datetime.datetime.strptime(current_date, "%Y-%m-%d")
            week_day = py_date.weekday()
            day = py_date.day
            if day > 22 and week_day > 2:
                self.position.close()


DATA_PATH = os.path.abspath('../../vn-stock-data/VNX/')
ticker_id = 'BVH'
ticker_data = _af.get_pricing_by_path(DATA_PATH + '/' + ticker_id + '.csv', '2010-01-01')
new_data = jModel.convertToJapanCandle(ticker_data)
bt = Backtest(ticker_data, Test, commission=.005, exclusive_orders=False)
stats = bt.run()
print(stats)
print(stats['_trades'])
bt.plot()
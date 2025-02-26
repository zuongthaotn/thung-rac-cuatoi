import warnings
warnings.filterwarnings('ignore')

import os
import sys

import method.algofuncs as _af

BACKTESTING_MODULE_PATH = os.path.abspath('backtest')
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
            bodies = self.data.Body
            ups = self.data.UpShadow
            lows = self.data.LowerShadow
            if(prices[-1] < prices[-2] and prices[-2] < prices[-3]):
                if(lows[-1] > 2 * bodies[-1]):
                    self.buy()
            if(prices[-1] > prices[-2] and prices[-2] > prices[-3]):
                if(lows[-1] > 2 * bodies[-1]):
                    self.position.close()

DATA_PATH = os.path.abspath('vn-stock-data/VNX/')
ticker_id = 'BVH'
ticker_data = _af.get_pricing_by_path(DATA_PATH + '/' + ticker_id+'.csv', '2018-01-01', '2021-10-05')
ticker_data['Height'] = ticker_data.apply(lambda x: x['High'] - x['Low'], axis = 1)
ticker_data['Body'] = ticker_data.apply(lambda x: abs(x['Close'] - x['Open']), axis = 1)
ticker_data['UpShadow'] = ticker_data.apply(lambda x: (x['High'] - x['Close']) if (x['Close'] > x['Open']) else (x['High'] - x['Open']), axis = 1)
ticker_data['LowerShadow'] = ticker_data.apply(lambda x: (x['Open'] - x['Low']) if (x['Close'] > x['Open']) else (x['Close'] - x['Low']), axis = 1)
bt = Backtest(ticker_data, Test, commission=.005, exclusive_orders=False)
stats = bt.run()
print(stats)
bt.plot()
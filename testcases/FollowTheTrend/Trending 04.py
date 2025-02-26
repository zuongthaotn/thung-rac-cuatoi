import warnings
warnings.filterwarnings('ignore')

import os
import sys
import pandas as pd

BACKTESTING_MODULE_PATH = os.path.abspath('../../backtest')
sys.path.insert(1, BACKTESTING_MODULE_PATH)
from backtesting.backtesting import Backtest, Strategy

METHOD_MODULE_PATH = os.path.abspath('../..')
sys.path.insert(1, METHOD_MODULE_PATH)
import method.Ticker as Ticker
import method.SaleRules as _sr
import method.algofuncs as _af
path = os.getcwd()
class FollowTheTrend(Strategy):
    def init(self):
        self.buy_price = 0
        self._index = 0
    def next(self):
        prices = self.data.Close
        opens = self.data.Open
        volumes = self.data.Volume
        lows = pd.DataFrame(data=self.data.Low).Low
        highs = pd.DataFrame(data=self.data.High).High
        if len(prices) > 23:
            last_price = prices[-1]
            atr_22 = _sr.getATR(22, highs, lows)
            if self.buy_price == 0 and Ticker.isFollowTrendingV2(prices, volumes, opens[-1], 2.5):
                self.buy_price = last_price
                self.buy()
            if self.buy_price != 0 and ((_sr.takeProfitByPercent(5, last_price, self.buy_price) and opens[-1] < prices[-1] and abs(highs.iloc[-1] - lows.iloc[-1]) > 2*atr_22 ) or _sr.shouldCutLossByPercent(8, last_price, self.buy_price)):
            # if self.buy_price != 0 and ((_sr.takeProfitByPercent(5, last_price, self.buy_price) and abs(highs.iloc[-1] - lows.iloc[-1]) > 2*atr_22 ) or _sr.shouldCutLossByPercent(8, last_price, self.buy_price)):
                self.position.close()
                self.buy_price = 0

ticker_id = 'PNJ'
DATA_PATH = os.path.abspath('../../vn-stock-data/VNX/')
ticker = _af.get_pricing_by_path(DATA_PATH + '/' + ticker_id+'.csv', '2010-01-01', '2020-10-05')
bt = Backtest(ticker, FollowTheTrend, commission=.005, exclusive_orders=False)
stats = bt.run()
bt.plot()
print(stats)
# print(stats['_trades'])
# new_file = path+"/result_"+ticker_id+".csv"
# stats['_trades'].to_csv(new_file, index=False)
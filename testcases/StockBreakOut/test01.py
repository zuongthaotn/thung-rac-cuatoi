import warnings
warnings.filterwarnings('ignore')

import os
import sys

BACKTESTING_MODULE_PATH = os.path.abspath('../../backtest')
sys.path.insert(1, BACKTESTING_MODULE_PATH)
from backtesting.backtesting import Backtest, Strategy

METHOD_MODULE_PATH = os.path.abspath('../..')
sys.path.insert(1, METHOD_MODULE_PATH)
import method.Ticker as Ticker
import method.SaleRules as _sr
import method.algofuncs as _af
path = os.getcwd()


path = os.getcwd()
class FollowTheTrend(Strategy):
    def init(self):
        self.buy_price = 0
        self._index = 0
    def next(self):
        prices = self.data.Close
        opens = self.data.Open
        volumes = self.data.Volume
        if len(self.data.Volume) > 66:
            last_price = prices[-1]
            if self.buy_price == 0 and Ticker.isStockOut(prices):
                self.buy_price = last_price
                self.buy()
            if self.buy_price != 0 and (_sr.takeProfitByPercent(5, last_price, self.buy_price) or _sr.shouldCutLossByPercent(8, last_price, self.buy_price)):
                self.position.close()
                self.buy_price = 0

ticker_id = 'VNM'
DATA_PATH = os.path.abspath('../../vn-stock-data/VNX/')
ticker = _af.get_pricing_by_path(DATA_PATH + '/' + ticker_id+'.csv', '2019-01-01', '2020-12-05')
bt = Backtest(ticker, FollowTheTrend, commission=.005, exclusive_orders=False)
stats = bt.run()
# bt.plot()
print(stats)
# print(stats['Sharpe Ratio'])
new_file = path+"/result_"+ticker_id+".csv"
stats['_trades'].to_csv(new_file, index=False)

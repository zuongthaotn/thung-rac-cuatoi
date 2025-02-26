import os
from backtesting import Backtest, Strategy
from backtesting.magnus import _read_file

import method.Ticker as Ticker
import method.TakeProfit as TakeProfit
import method.CutLoss as CutLoss

path = os.getcwd()
class FollowTheTrend(Strategy):
    def init(self):
        self.buy_price = 0
        self._index = 0
    def next(self):
        prices = self.data.Close
        opens = self.data.Open
        volumes = self.data.Volume
        if len(self.data.Volume) > 5:
            last_price = prices[-1]
            if self.buy_price == 0 and Ticker.isFollowTrendingV2(prices, volumes, opens[-1], 2.5):
                self.buy_price = last_price
                self.buy()
            if self.buy_price != 0 and (TakeProfit.takeProfit(5, last_price, self.buy_price) or CutLoss.shouldCutLossByPercent(8, last_price, self.buy_price)):
                self.position.close()
                self.buy_price = 0
vn30_ticker = Ticker.getListVN30()
for ticker in vn30_ticker:
    BID = _read_file(ticker+'.csv')
    bt = Backtest(BID, FollowTheTrend, commission=.005, exclusive_orders=False)
    stats = bt.run()
    # bt.plot()
    print(ticker)
    print(stats['Sharpe Ratio'])
    # # print(stats['_trades'])
    # new_file = path+"/testcases/FollowTheTrend/result_"+ticker+".csv"
    # stats['_trades'].to_csv(new_file, index=False)

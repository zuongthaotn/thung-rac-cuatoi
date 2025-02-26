import os
import numpy as np
from backtesting import Backtest, Strategy

from backtesting.magnus import get_pricing
from backtesting.test import SMA
from backtesting.lib import crossover
import method.Ticker as Ticker
import method.TakeProfit as TakeProfit
import method.CutLoss as CutLoss

path = os.getcwd()
class FollowTheTrend(Strategy):
    def init(self):
        price = self.data.Close
        self.buy_price = 0
        self._index = 0
        self.ma1 = self.I(SMA, price, 10)
        self.ma2 = self.I(SMA, price, 20)

    def next(self):
        prices = self.data.Close
        opens = self.data.Open
        volumes = self.data.Volume
        # self._index = self._index + 1
        # print("----------"+str(self._index)+"--------")
        if len(self.data.Volume) > 5:
            last_5_volumes = volumes[-5::]
            last_3_prices = prices[-3::]
            # min_volume = min(last_5_volumes)
            max_volume = max(last_5_volumes)
            last_volume = last_5_volumes[-1]
            mean_f = np.mean(volumes[-5:-2])
            last_open_price = opens[-1]
            last_price = prices[-1]
            if self.buy_price == 0 and Ticker.isFollowTrendingV2(prices, volumes, opens[-1], 2.5):
                self.buy_price = last_price
                self.buy()
            # if self.buy_price != 0 and (TakeProfit.takeProfit(5, last_price, self.buy_price) or CutLoss.shouldCutLossByPercent(8,last_price,self.buy_price)):
            if self.buy_price != 0 and (crossover(self.ma2, self.ma1) or CutLoss.shouldCutLossByPercent(8, last_price, self.buy_price)):
                self.position.close()
                self.buy_price = 0

ticker_id = 'VHM'
ticker = get_pricing(ticker_id+'.csv', '2020-01-01', '2020-10-05')
bt = Backtest(ticker, FollowTheTrend, cash=10000, commission=.005, exclusive_orders=False)
stats = bt.run()
bt.plot()
print(stats)
# # print(stats['_trades'])
# new_file = path+"/result_"+ticker_id+".csv"
# stats['_trades'].to_csv(new_file, index=False)

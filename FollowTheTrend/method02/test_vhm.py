import numpy as np
from backtesting import Backtest, Strategy

from backtesting.magnus import _read_file


class FollowTheTrend(Strategy):
    def init(self):
        self.buy_price = 0
        self._index = 0
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
            if last_3_prices[0] < last_3_prices[1] and last_3_prices[0] < last_3_prices[
                2] and last_volume == max_volume and last_volume > 2.5 * mean_f and last_volume > 1000000 and last_open_price < \
                    last_3_prices[2]:
                self.buy_price = last_price
                # print("buy date:" + str(self.data.index[-1]))
                self.buy()
            if self.buy_price != 0 and (last_price > 1.05 * self.buy_price or last_price < 0.9 * self.buy_price):
                # print("sell date:" + str(self.data.index[-1]))
                # print("buy price:" + str(self.buy_price))
                # print("sell price:" + str(self.last_price))
                # self.sell()
                self.position.close()
                self.buy_price = 0

VHM = _read_file('VHM.csv')
bt = Backtest(VHM, FollowTheTrend, commission=.002,
              exclusive_orders=True)
stats = bt.run()
# bt.plot()
print(stats)
# # print(stats['_trades'])
new_file = "result_VHM.csv"
stats['_trades'].to_csv(new_file, index=False)

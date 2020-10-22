import numpy as np
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

from backtesting.magnus import SMA, BID


class SmaCross(Strategy):
    def init(self):
        self._index = 0
    def next(self):
        self._index = self._index + 1
        print(self._index)


bt = Backtest(BID, SmaCross, commission=.002,
              exclusive_orders=True)
stats = bt.run()
# bt.plot()
# print(stats)
#print(stats['_trades'])

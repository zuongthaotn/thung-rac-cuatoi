import os
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

import method.TakeProfit as TakeProfit
import method.CutLoss as CutLoss
from backtesting.test import SMA
from backtesting.magnus import _read_file

path = os.getcwd()
class SmaCross(Strategy):
    def __init__(self, broker, data, params):
        super().__init__(broker, data, params)
        self.buy_price = 0

    def init(self):
        price = self.data.Close
        self.ma1 = self.I(SMA, price, 10)
        self.ma2 = self.I(SMA, price, 30)
        self.ma3 = self.I(SMA, price, 100)
        self.ma4 = self.I(SMA, price, 200)

    def next(self):
        prices = self.data.Close
        last_price = prices[-1]
        # if self.buy_price == 0 and crossover(self.ma1, self.ma2) and crossover(prices, self.ma3) and crossover(prices, self.ma4):
        if self.buy_price == 0 and crossover(self.ma1, self.ma2):
            self.buy()
            self.buy_price = last_price
        elif self.buy_price != 0 and (TakeProfit.takeProfit(5, last_price, self.buy_price) or CutLoss.shouldCutLossByPercent(8, last_price, self.buy_price)):
            self.position.close()
            self.buy_price = 0


BID = _read_file('BID.csv')
bt = Backtest(BID, SmaCross, commission=.005, exclusive_orders=False)
stats = bt.run()
bt.plot()
print(stats)
#print(stats['_trades'])
new_file = path+"/result_BID.csv"
stats['_trades'].to_csv(new_file, index=False)
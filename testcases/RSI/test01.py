import os
from backtesting import Backtest, Strategy
from backtesting.magnus import _read_file

import method.Ticker as Ticker
import method.TakeProfit as TakeProfit
import method.CutLoss as CutLoss

path = os.getcwd()
class RSIuptrending(Strategy):
    def init(self):
        self.buy_price = 0
        self._index = 0
    def next(self):
        prices = self.data.Close
        if len(self.data.Volume) > 14:
            last_price = prices[-1]
            if self.buy_price == 0 and Ticker.isPriceUpTrendByRSI12D(prices) == True:
                self.buy_price = last_price
                self.buy()
            # if self.buy_price != 0 and (TakeProfit.takeProfit(5, last_price, self.buy_price) or CutLoss.shouldCutLossByPercent(8, last_price, self.buy_price)):
            if self.buy_price != 0 and Ticker.isPriceUpTrendByRSI12D(prices) == False:
                self.position.close()
                self.buy_price = 0

best_return = 0
best_return_ticker = ''
all_ticker = Ticker.getAllTickers('/home/zuongthao/GIT/zuongthaotn/backtesting.py/method/VNX.csv')
for ticker in all_ticker:
    ticker_data = _read_file(ticker+'.csv')
    bt = Backtest(ticker_data, RSIuptrending, commission=.005, exclusive_orders=False)
    stats = bt.run()
    # bt.plot()
    # print(stats)
    # exit()
    if stats['Return [%]'] > best_return:
        best_return_ticker = ticker
        # print(ticker)
        # print(stats['Sharpe Ratio'])
    # # print(stats['_trades'])
    # new_file = path+"/result_"+ticker+".csv"
    # stats['_trades'].to_csv(new_file, index=False)
print(best_return_ticker)
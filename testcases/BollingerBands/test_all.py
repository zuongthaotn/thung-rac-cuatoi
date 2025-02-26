import os
from backtesting import Backtest, Strategy
from backtesting.magnus import _read_file

import method.Ticker as Ticker
import method.TakeProfit as TakeProfit
import method.CutLoss as CutLoss

path = os.getcwd()
class BollingerBands(Strategy):
    def init(self):
        self.buy_price = 0
        self._index = 0
    def next(self):
        prices = self.data.Close
        if len(self.data.Volume) > 19:
            last_price = prices[-1]
            if self.buy_price == 0 and Ticker.hasSignalByBollingerBandsV1(prices) == 1:
                self.buy_price = last_price
                self.buy()
            if self.buy_price != 0 and Ticker.hasSignalByBollingerBandsV1(prices) == -1:
                self.position.close()
                self.buy_price = 0


best_return = 0
best_return_ticker = ''
all_ticker = Ticker.getAllTickers('/home/zuongthao/GIT/zuongthaotn/backtesting.py/method/VNX.csv')
for ticker in all_ticker:
    ticker_data = _read_file(ticker+'.csv')
    bt = Backtest(ticker_data, BollingerBands, commission=.005, exclusive_orders=False)
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
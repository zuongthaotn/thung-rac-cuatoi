import warnings

warnings.filterwarnings('ignore')

import os
import sys
import pandas as pd

METHOD_MODULE_PATH = os.path.abspath('.')
sys.path.insert(1, METHOD_MODULE_PATH)
import vn_realtime_stock_data.stockHistory as stockHistory

ticker = 'ACB'
htd = stockHistory.getAllStockHistoryData(ticker)  # not include today data
if 'Time' in htd.columns:
    from datetime import datetime

    htd['DateStr'] = htd.apply(
        lambda x: datetime.fromtimestamp(x['Time']).strftime("%Y-%m-%d"), axis=1)
htd['SMA_5'] = htd['Close'].rolling(window=5).mean()
htd['SMA_20'] = htd['Close'].rolling(window=20).mean()
htd['Date'] = pd.to_datetime(htd['DateStr'])
ticker_data = htd.set_index('Date')
ticker_data.drop(['Time'], axis=1)
ticker_data.drop(['DateStr'], axis=1)
ticker_data['Date'] = pd.to_datetime(ticker_data.index)

BACKTESTING_MODULE_PATH = os.path.abspath('backtest')
sys.path.insert(1, BACKTESTING_MODULE_PATH)
from backtesting.backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA


class Sma07(Strategy):
    def init(self):
        price = self.data.Close
        self.buy_price = 0
        self.cross_price = 0
        self.sma_cross = 0
        self.ma5 = self.I(SMA, price, 5)
        self.ma20 = self.I(SMA, price, 20)

    def next(self):
        close_price = self.data.Close[-1]
        yesterday_close_price = self.data.Close[-2]
        last_sma5 = self.ma5[-1]
        last_sma20 = self.ma20[-1]
        if crossover(self.ma5, self.ma20):
            self.sma_cross = 1
            self.cross_price = last_sma5
        if self.buy_price == 0 and self.sma_cross == 1 and (last_sma5 - last_sma20) / yesterday_close_price > 0.04:
            self.buy()
            self.buy_price = close_price
        elif self.buy_price != 0 and (crossover(self.ma20, self.data.Close) or close_price < .99 * self.ma5[-1]):
            self.position.close()
            self.buy_price = 0

bt = Backtest(ticker_data, Sma07)
stats = bt.run()
# print(stats['_trades'])
bt.plot()
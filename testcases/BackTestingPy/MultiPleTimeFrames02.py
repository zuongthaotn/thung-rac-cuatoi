import warnings

warnings.filterwarnings('ignore')

import os
import sys
import pandas as pd

METHOD_MODULE_PATH = os.path.abspath('.')
sys.path.insert(1, METHOD_MODULE_PATH)
import vn_realtime_stock_data.stockHistory as stockHistory

ticker = 'POW'
htd = stockHistory.getStockHistoryData(ticker)  # not include today data
if 'Time' in htd.columns:
    from datetime import datetime

    htd['DateStr'] = htd.apply(
        lambda x: datetime.fromtimestamp(x['Time']).strftime("%Y-%m-%d"), axis=1)
htd['Date'] = pd.to_datetime(htd['DateStr'])
ticker_data = htd.set_index('Date')
ticker_data.drop(['Time'], axis=1)
ticker_data.drop(['DateStr'], axis=1)
ticker_data['Date'] = pd.to_datetime(ticker_data.index)


def SMA(array, n):
    """Simple moving average"""
    return pd.Series(array).rolling(n).mean()


def RSI(array, n):
    """Relative strength index"""
    # Approximate; good enough
    gain = pd.Series(array).diff()
    loss = gain.copy()
    gain[gain < 0] = 0
    loss[loss > 0] = 0
    rs = gain.ewm(n).mean() / loss.abs().ewm(n).mean()
    return 100 - 100 / (1 + rs)


BACKTESTING_MODULE_PATH = os.path.abspath('backtest')
sys.path.insert(1, BACKTESTING_MODULE_PATH)
from backtesting.backtesting import Backtest, Strategy
from backtesting.lib import resample_apply

class System(Strategy):
    d_rsi = 30  # Daily RSI lookback periods
    w_rsi = 30  # Weekly
    level = 70

    def init(self):
        # Compute moving averages the strategy demands
        self.ma10 = self.I(SMA, self.data.Close, 10)
        self.ma20 = self.I(SMA, self.data.Close, 20)
        self.ma50 = self.I(SMA, self.data.Close, 50)
        self.ma100 = self.I(SMA, self.data.Close, 100)

        # Compute daily RSI(30)
        self.daily_rsi = self.I(RSI, self.data.Close, self.d_rsi)

        # To construct weekly RSI, we can use `resample_apply()`
        # helper function from the library
        self.weekly_rsi = resample_apply(
            'W-FRI', RSI, self.data.Close, self.w_rsi)

    def next(self):
        price = self.data.Close[-1]

        # If we don't already have a position, and
        # if all conditions are satisfied, enter long.
        if (not self.position and
                self.daily_rsi[-1] > self.level and
                self.weekly_rsi[-1] > self.level and
                self.weekly_rsi[-1] > self.daily_rsi[-1] and
                self.ma100[-1] < self.ma50[-1] < self.ma20[-1] < self.ma10[-1] < price):

            # Buy at market price on next open, but do
            # set 8% fixed stop loss.
            self.buy(sl=.92 * price)

        # If the price closes 2% or more below 10-day MA
        # close the position, if any.
        elif price < .98 * self.ma10[-1]:
            self.position.close()


backtest = Backtest(ticker_data, System, commission=.005, exclusive_orders=False)
stats = backtest.run()
print(stats)
optimized_stats = backtest.optimize(d_rsi=range(10, 35, 5),
                  w_rsi=range(10, 35, 5),
                  level=range(30, 80, 10))
print(optimized_stats)
backtest.plot()

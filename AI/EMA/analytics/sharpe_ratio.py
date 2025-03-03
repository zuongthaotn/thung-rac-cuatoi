import warnings
warnings.filterwarnings('ignore')

import datetime
import time

import sys
import sys_path
sys.path.insert(1, sys_path.BACKTESTING_MODULE_PATH)

from backtest.backtesting.backtesting import Backtest, Strategy
import vn_realtime_stock_data.stockHistory as stockHistory
import vn_realtime_stock_data.stockRealtimes as stockRealtime

import method.EMA.v1 as ema_v1
import AI.EMA.sources.signal as signal
import AI.EMA.sources.constants as constants

class EmaRsi(Strategy):
    def init(self):
        self.buy_price = 0

    def next(self):
        if (len(self.data.Close) < 23):
            return
        emaR = self.data.EMA_R
        emaR_2 = emaR[-3]
        emaR_yesterday = emaR[-2]
        emaR_today = emaR[-1]
        rsi = self.data.RSI_mini
        rsi_today = rsi[-1]
        stock_market_signal = signal.get_signal(emaR_2, emaR_yesterday, emaR_today, rsi_today)
        if self.buy_price == 0 and stock_market_signal[0] >= constants.BUY_SIGNAL_LINE:
            self.buy()
            self.buy_price = self.data.Close[-1]
        if self.buy_price != 0 and stock_market_signal[0] <= constants.SELL_SIGNAL_LINE:
            self.position.close()
            self.buy_price = 0


love_list = stockRealtime.get_vn100_tickers()
date_from = constants.TEST_FROM_DATE
timestamp_from = time.mktime(datetime.datetime.strptime(date_from, "%d/%m/%Y").timetuple())
date_to = constants.TEST_TO_DATE
timestamp_to = time.mktime(datetime.datetime.strptime(date_to, "%d/%m/%Y").timetuple())

rows = []
for ticker in love_list:
    htd = stockHistory.getStockHistoryData(ticker, timestamp_from, timestamp_to)
    prepared_data = ema_v1.prepareData(htd)
    emaR = prepared_data['EMA_R']
    rsi = prepared_data['RSI_mini']
    rows_number = len(prepared_data.index)
    signal.set_ticker(ticker)
    signal.reset_network()
    signal.set_is_debug_mode(True)
    if not signal.is_trained():
        continue
    bt = Backtest(prepared_data, EmaRsi)
    stats = bt.run()

    rows.append(
        [ticker, stats['Return (Ann.) [%]'], stats['Return [%]'], stats['Sharpe Ratio'], stats['Sortino Ratio'],
         stats['Calmar Ratio']])
    time.sleep(1)

import pandas as pd
df = pd.DataFrame(rows, columns=['Ticker', 'Return (Ann.)', 'Return', 'Sharpe Ratio', 'Sortino Ratio', 'Calmar Ratio'])

import os
new_file = os.path.join(constants.ROOT_DIR, "resources", 'Ratio_reports.csv')
df.to_csv(new_file, index=False)

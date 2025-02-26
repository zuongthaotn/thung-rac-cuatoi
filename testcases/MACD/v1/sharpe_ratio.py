import sys
import sys_path
import warnings
warnings.filterwarnings('ignore')

from datetime import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
import time

sys.path.insert(1, sys_path.BACKTESTING_MODULE_PATH)
from backtesting.backtesting import Backtest, Strategy
import vn_realtime_stock_data.stockHistory as stockHistory
import vn_realtime_stock_data.stockRealtimes as stockRealtime
import method.MACD.v1 as v1


class Macd(Strategy):
    def init(self):
        self.buy_price = 0
        self.current_price = 0

    def next(self):
        self.current_price = self.data.Close[-1]
        if self.buy_price == 0 and v1.hasBuySignal(self.data.MACD, self.data.MACDs):
            self.buy()
            self.buy_price = self.data.Close[-1]
        elif self.buy_price != 0 and (v1.has_force_sell_signal(self.current_price, self.buy_price) or v1.hasSellSignal(self.data.MACD, self.data.MACDs)):
            self.position.close()
            self.buy_price = 0

love_list = []
for exchange in ['hose', 'hnx', 'upcom']:
    multi_ticket_data = stockRealtime.getTodayData(exchange)
    for ticker_data in multi_ticket_data:
        ticker = ticker_data['stockSymbol']
        if len(ticker) != 3:
            continue
        _volume = ticker_data['nmTotalTradedQty']
        if type(_volume) is not int:
            continue
        if _volume < 1000000:
            continue
        love_list.append(ticker)

two_years = date.today() + relativedelta(years=-3)
timestamp_from = datetime.strptime(two_years.strftime("%m/%d/%Y") + ', 00:00:0', "%m/%d/%Y, %H:%M:%S").timestamp()
timestamp_to = datetime.strptime(date.today().strftime("%m/%d/%Y") + ', 23:59:00', "%m/%d/%Y, %H:%M:%S").timestamp()

rows = []
for ticker_id in love_list:
    htd = stockHistory.getStockHistoryData(ticker_id, 1, timestamp_to)
    prepared_data = v1.prepareData(htd)
    bt = Backtest(prepared_data, Macd)
    stats = bt.run()

    if (stats['Sharpe Ratio'] > 0.5):
        rows.append([ticker_id, stats['Return (Ann.) [%]'], stats['Return [%]'], stats['Sharpe Ratio'], stats['Sortino Ratio'], stats['Calmar Ratio']])
    time.sleep(1)

import pandas as pd
df = pd.DataFrame(rows, columns=['Ticker', 'Return (Ann.)', 'Return', 'Sharpe Ratio', 'Sortino Ratio', 'Calmar Ratio'])
import os
local_dir = os.path.dirname(__file__)
new_file = os.path.join(local_dir, 'Ratio_reports.csv')
df.to_csv(new_file, index=False)

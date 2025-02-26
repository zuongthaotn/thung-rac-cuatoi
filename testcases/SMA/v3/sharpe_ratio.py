import sys
import sys_path
import warnings
warnings.filterwarnings('ignore')

from datetime import datetime
from datetime import date
from dateutil.relativedelta import relativedelta

sys.path.insert(1, sys_path.BACKTESTING_MODULE_PATH)
from backtesting.backtesting import Backtest, Strategy
import vn_realtime_stock_data.stockHistory as stockHistory
import vn_realtime_stock_data.stockRealtimes as stockRealtime
import method.SMA.v3 as v3


class Sma(Strategy):
    cutoff_percent = 0.99
    def init(self):
        self.buy_price = 0

    def next(self):
        if (len(self.data.SMA_H) < 21):
            return
        if self.buy_price == 0 and v3.hasBuySignal(self.data.SMA_H):
            self.buy()
            self.buy_price = self.data.Close[-1]
        elif self.buy_price != 0 and v3.hasSellSignal(self.data.Open, self.data.Close, self.data.SMA_H, self.data.SMA_5,
                                                      self.data.SMA_20,
                                                      cutoff_percent=self.cutoff_percent):
            self.position.close()
            self.buy_price = 0

love_list = []
multi_ticket_data = stockRealtime.getTodayData('hose')
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
    htd = stockHistory.getStockHistoryData(ticker_id, timestamp_from, timestamp_to)
    prepared_data = v3.prepareData(htd)
    bt = Backtest(prepared_data, Sma)
    stats = bt.run()

    # initialize list of lists
    rows.append([ticker_id, stats['Return [%]'], stats['Sharpe Ratio'], stats['Sortino Ratio'], stats['Calmar Ratio']])

import pandas as pd
df = pd.DataFrame(rows, columns=['Ticker', 'Return', 'Sharpe Ratio', 'Sortino Ratio', 'Calmar Ratio'])
import os
local_dir = os.path.dirname(__file__)
new_file = os.path.join(local_dir, 'Ratio_reports.csv')
df.to_csv(new_file, index=False)

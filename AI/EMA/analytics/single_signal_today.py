import os
import time

import warnings
warnings.filterwarnings('ignore')

import sys
from pathlib import Path
ALGO_PATH = os.path.abspath(Path(__file__).parent.parent.parent.parent)
if ALGO_PATH not in sys.path:
    sys.path.insert(1, ALGO_PATH)

import vn_realtime_stock_data.stockHistory as stockHistory
import vn_realtime_stock_data.stockRealtimes as stockRealtime
import method.EMA.v1 as ema_v1
import AI.EMA.sources.signal as signal

from datetime import datetime
from datetime import date
from dateutil.relativedelta import relativedelta

tickers = stockRealtime.get_vn100_tickers()

date_from = date.today() + relativedelta(months=-3)
timestamp_from = datetime.strptime(date_from.strftime("%m/%d/%Y") + ', 00:00:0', "%m/%d/%Y, %H:%M:%S").timestamp()
date_to = date.today()
timestamp_to = datetime.strptime(date_to.strftime("%m/%d/%Y") + ', 23:59:00', "%m/%d/%Y, %H:%M:%S").timestamp()
message = '(EMA_RSI.AI.v1)Report single signal: \n'
ticker = 'ACB'
signal.set_ticker(ticker)
signal.reset_network()
if not signal.is_trained():
    exit()
htd = stockHistory.getStockHistoryData(ticker, timestamp_from, timestamp_to)
prepared_data = ema_v1.prepareData(htd)
rows_number = len(prepared_data.index)
emaR = prepared_data['EMA_R']
rsi = prepared_data['RSI_mini']
emaR_3 = emaR[-4]
emaR_2 = emaR[-3]
emaR_yesterday = emaR[-2]
emaR_today = emaR[-1]
rsi_yesterday = rsi[-2]
rsi_today = rsi[-1]
yesterday_stock_market_signal = signal.get_signal(emaR_3, emaR_2, emaR_yesterday, rsi_yesterday)[0]
today_stock_market_signal = signal.get_signal(emaR_2, emaR_yesterday, emaR_today, rsi_today)[0]
message += ticker + "\n"
message += "Yesterday signal: " + str(yesterday_stock_market_signal) + ")\n"
message += "Today signal: " + str(today_stock_market_signal) + ")\n"
print(message)
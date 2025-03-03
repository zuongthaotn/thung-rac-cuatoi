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
import AI.EMA.sources.constants as constants

from datetime import datetime
from datetime import date
from dateutil.relativedelta import relativedelta

tickers = stockRealtime.get_vn100_tickers()

date_from = date.today() + relativedelta(months=-3)
timestamp_from = datetime.strptime(date_from.strftime("%m/%d/%Y") + ', 00:00:0', "%m/%d/%Y, %H:%M:%S").timestamp()
date_to = date.today()
timestamp_to = datetime.strptime(date_to.strftime("%m/%d/%Y") + ', 23:59:00', "%m/%d/%Y, %H:%M:%S").timestamp()
selectedTickers = []
message = '(EMA_RSI.AI.v1)Report single ticker signal history: \n'
ticker = 'VRE'
message += ticker + "\n"
signal.set_ticker(ticker)
signal.reset_network()
if not signal.is_trained():
    exit()
htd = stockHistory.getStockHistoryData(ticker, timestamp_from, timestamp_to)
prepared_data = ema_v1.prepareData(htd)
rows_number = len(prepared_data.index)
emaR = prepared_data['EMA_R']
rsi = prepared_data['RSI_mini']
the_last_signal_is = ''
for i in range(3, rows_number):
    stock_market_signal_i = signal.get_signal(emaR[i - 2], emaR[i - 1], emaR[i], rsi[i])[0]
    if stock_market_signal_i <= constants.SELL_SIGNAL_LINE:
        the_last_signal_is = "Sell"
    if stock_market_signal_i >= constants.BUY_SIGNAL_LINE:
        the_last_signal_is = "Buy"
    message += "Date {} signal {} \n" .format(prepared_data.index[i], stock_market_signal_i)
print(message)
print("The last signal is: {}".format(the_last_signal_is))
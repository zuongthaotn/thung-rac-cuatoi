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
import AI.EMA.sources.constants as constants
import AI.EMA.sources.signal as signal

from datetime import datetime
from datetime import date
from dateutil.relativedelta import relativedelta

tickers = stockRealtime.get_vn100_tickers()

date_from = date.today() + relativedelta(months=-3)
timestamp_from = datetime.strptime(date_from.strftime("%m/%d/%Y") + ', 00:00:0', "%m/%d/%Y, %H:%M:%S").timestamp()
date_to = date.today()
timestamp_to = datetime.strptime(date_to.strftime("%m/%d/%Y") + ', 23:59:00', "%m/%d/%Y, %H:%M:%S").timestamp()
selectedTickers = []
message = '(EMA_RSI.AI.v1)Những cổ phiếu đang rảnh rỗi: \n'
end_message = ''
for ticker in tickers:
    signal.set_ticker(ticker)
    signal.reset_network()
    if not signal.is_trained():
        continue
    time.sleep(1)
    htd = stockHistory.getStockHistoryData(ticker, timestamp_from, timestamp_to)
    prepared_data = ema_v1.prepareData(htd)
    rows_number = len(prepared_data.index)
    emaR = prepared_data['EMA_R']
    rsi = prepared_data['RSI_mini']
    last_one_is_sell = False
    for i in range(rows_number-2, 23, -1):
        stock_market_signal_i = signal.get_signal(emaR[i - 2], emaR[i - 1], emaR[i], rsi[i])[0]
        # print("------------------ Ticker: {} has signal {} in {}".format(ticker, stock_market_signal_i, prepared_data['Date'][i]))
        if stock_market_signal_i <= constants.SELL_SIGNAL_LINE:
            # print("Ticker: {} was sold the last in {}" . format(ticker, prepared_data['Date'][i]))
            last_one_is_sell = True
            break
        if stock_market_signal_i >= constants.BUY_SIGNAL_LINE:
            # print("Ticker: {} was bought the last in {}" . format(ticker, prepared_data['Date'][i]))
            end_message += "Ticker: {} was bought the last in {} with price {}.\n" . format(ticker, prepared_data['Date'][i], prepared_data['Close'][i])
            today_stock_market_signal = signal.get_signal(emaR[-3], emaR[-2], emaR[-1], rsi[-1])[0]
            end_message += "Today signal: {}\n" . format(today_stock_market_signal)
            end_message += "Bought price {}. Today price: {}\n" . format(prepared_data['Close'][i], prepared_data['Close'][-1])
            last_one_is_sell = False
            break
    if last_one_is_sell:
        emaR_2 = emaR[-3]
        emaR_yesterday = emaR[-2]
        emaR_today = emaR[-1]
        rsi_today = rsi[-1]
        today_stock_market_signal = signal.get_signal(emaR_2, emaR_yesterday, emaR_today, rsi_today)[0]
        selectedTickers.append(ticker)
        message += ticker + "(s:" + str(today_stock_market_signal) + ", p:" + str(prepared_data['Close'][-1]) + ")\n"

# print(message)
import os
txt_file = os.path.join(constants.ROOT_DIR, "resources", 'tickers_free.html')
if selectedTickers:
    # Open the file in write mode (this will overwrite the file)
    with open(txt_file, 'w') as file:
        # Write new content to the file
        file.write(message)
with open(txt_file, 'a') as file:
    # Write new content to the file
    file.write(end_message)
print("Done!")

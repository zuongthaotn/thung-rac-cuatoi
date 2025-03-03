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

import gsheet.service as gSheetService
sheet_data = gSheetService.get_data("1roOZQvWo4g_M6uZj6t-3jriELM_pmkizt7b4k9Ni2VQ", "A1:D")
buy_list = sheet_data.Ticker.values.tolist()
if not buy_list:
    print("Error 1")
    exit()

tickers = stockRealtime.get_vn100_tickers()
if not tickers:
    print("Error 2")
    exit()

date_from = date.today() + relativedelta(months=-3)
timestamp_from = datetime.strptime(date_from.strftime("%m/%d/%Y") + ', 00:00:0', "%m/%d/%Y, %H:%M:%S").timestamp()
date_to = date.today()
timestamp_to = datetime.strptime(date_to.strftime("%m/%d/%Y") + ', 23:59:00', "%m/%d/%Y, %H:%M:%S").timestamp()
selectedTickers = []
message = '(EMA_RSI.AI.v1)Những cổ phiếu đc xem xét: \n'
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
    emaR_2 = emaR[-3]
    emaR_yesterday = emaR[-2]
    emaR_today = emaR[-1]
    rsi_today = rsi[-1]

    today_stock_market_signal = signal.get_signal(emaR_2, emaR_yesterday, emaR_today, rsi_today)[0]

    if today_stock_market_signal <= constants.SELL_SIGNAL_LINE:
        if ticker in buy_list:
            selectedTickers.append(ticker)
            message += ticker + "(" + str(prepared_data['Close'][-1]) + ")(BÁN)\n"
    else:
        if today_stock_market_signal >= constants.BUY_SIGNAL_LINE:
            if ticker not in buy_list:
                last_one_is_sell = False
                for i in range(rows_number-2, 23, -1):
                    stock_market_signal_i = signal.get_signal(emaR[i - 2], emaR[i - 1], emaR[i], rsi[i])
                    if stock_market_signal_i[0] <= constants.SELL_SIGNAL_LINE:
                        # print("Ticker: {} was sold the last in {}" . format(ticker, prepared_data['Date'][i]))
                        last_one_is_sell = True
                        break
                    if stock_market_signal_i[0] >= constants.BUY_SIGNAL_LINE:
                        # print("Ticker: {} was bought the last in {}" . format(ticker, prepared_data['Date'][i]))
                        last_one_is_sell = False
                        break
                if last_one_is_sell and ticker not in buy_list:
                    selectedTickers.append(ticker)
                    message += ticker + "(" + str(prepared_data['Close'][-1]) + ")(MUA)\n"

if selectedTickers:
    # print(message)
    print(message)
print("Done!")

import time
import datetime

import sys
import os
from pathlib import Path
ALGO_PATH = os.path.abspath(Path(__file__).parent.parent.parent.parent)
if ALGO_PATH not in sys.path:
    sys.path.insert(1, ALGO_PATH)

import vn_realtime_stock_data.stockHistory as stockHistory
import method.EMA.v1 as ema_v1
import AI.EMA.sources.constants as constants
import AI.EMA.sources.signal as signal


def run():
    get_in = False
    buy_price = profit = 0
    transactions = []
    for i in range(23, rows_number):
        date = prepared_data.index[i]
        today_price = prepared_data['Close'][i]
        emaR_2 = emaR[i - 2]
        emaR_yesterday = emaR[i - 1]
        emaR_today = emaR[i]
        rsi_today = rsi[i]
        stock_market_signal = signal.get_signal(emaR_2, emaR_yesterday, emaR_today, rsi_today)
        # print("{} ---- {}" .format(date, stock_market_signal))
        if not get_in and stock_market_signal[0] > constants.BUY_SIGNAL_LINE:
            buy_price = today_price
            transactions.append("Buy --- {} --- with price {}".format(date, today_price))
            get_in = True
        if get_in and (stock_market_signal[0] <= constants.SELL_SIGNAL_LINE or i == rows_number-1):
            profit += (today_price - buy_price)
            transactions.append("Sell --- {} --- with price {}".format(date, today_price))
            get_in = False
            buy_price = 0
    print("Total profit: {}" . format(profit))
    print("Total Transactions:")
    for tran in transactions:
        print(tran)

if __name__ == '__main__':
    ticker = "ACB"
    # getting data for this generation
    date_from = "01/01/2022"
    timestamp_from = time.mktime(datetime.datetime.strptime(date_from, "%d/%m/%Y").timetuple())
    date_to = "31/12/2023"
    timestamp_to = time.mktime(datetime.datetime.strptime(date_to, "%d/%m/%Y").timetuple())
    htd = stockHistory.getStockHistoryData(ticker, timestamp_from, timestamp_to)
    print("Testing from {} to {}".format(date_from, date_to))
    prepared_data = ema_v1.prepareData(htd)
    emaR = prepared_data['EMA_R']
    rsi = prepared_data['RSI_mini']
    rows_number = len(prepared_data.index)
    signal.set_ticker(ticker)
    run()
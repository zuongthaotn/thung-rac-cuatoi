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
from AI.EMA.sources.broker import Broker
import AI.EMA.sources.signal as signal


def run():
    broker = Broker(constants.STARTING_CAPITAL)
    for i in range(22, rows_number):
        date = prepared_data.index[i]
        today_price = prepared_data['Close'][i]
        emaR_2 = emaR[i-2]
        emaR_yesterday = emaR[i-1]
        emaR_today = emaR[i]
        rsi_today = rsi[i]
        stock_market_signal = signal.get_signal(emaR_2, emaR_yesterday, emaR_today, rsi_today)
        broker.do_action(stock_market_signal, today_price, date)
        if i == rows_number-1:
            if broker.number_of_stocks:
                broker.sell_all_stocks(today_price, date)
    print("Final capital: {}" . format(broker.capital))
    print("Total Transactions:")
    for tran in broker.history:
        print(tran)

if __name__ == '__main__':
    ticker = "TPB"
    # getting data for this generation
    date_from = "01/01/2023"
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
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
import AI.EMA.sources.signal as signal

from bokeh.plotting import figure, show
from bokeh.layouts import column


def run():
    global prepared_data
    signal_line = []
    buy_line = []
    sell_line = []
    for i in range(0, rows_number):
        buy_line.append(0.9)
        sell_line.append(0.1)
        if i < 23:
            signal_line.append(0)
        else:
            emaR_2 = emaR[i - 2]
            emaR_yesterday = emaR[i - 1]
            emaR_today = emaR[i]
            rsi_today = rsi[i]
            stock_market_signal = signal.get_signal(emaR_2, emaR_yesterday, emaR_today, rsi_today)
            signal_line.append(stock_market_signal[0])

    prepared_data = prepared_data.assign(Signal=signal_line)
    prepared_data = prepared_data.assign(Sell_signal=sell_line)
    prepared_data = prepared_data.assign(Buy_signal=buy_line)

    # create a new plot with a datetime axis type
    s1 = figure(width=2000, height=250, x_axis_type="datetime")
    s1.line(prepared_data['Date'], prepared_data['Close'], color='navy', alpha=0.5)

    # create a new plot with a datetime axis type
    s2 = figure(width=2000, height=250, x_axis_type="datetime")
    s2.line(prepared_data['Date'], prepared_data['Signal'], color='red', alpha=0.5)
    s2.line(prepared_data['Date'], prepared_data['Buy_signal'], color='green', alpha=0.5)
    s2.line(prepared_data['Date'], prepared_data['Sell_signal'], color='blue', alpha=0.5)

    # put all the plots in a VBox
    p = column(s1, s2)

    # show the results
    show(p)

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
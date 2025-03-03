import time
from datetime import datetime

import numpy as np
import pandas_ta as ta
import pandas as pd

import sys
import os
from pathlib import Path
ALGO_PATH = os.path.abspath(Path(__file__).parent.parent.parent.parent)
if ALGO_PATH not in sys.path:
    sys.path.insert(1, ALGO_PATH)

import vn_realtime_stock_data.stockHistory as stockHistory
import AI.VN30ps.neat.sources.signal as signal


def run():
    total_predict_success = 0
    total_predict_false = 0
    for i in range(23, rows_number):
        date = prepared_data.index[i]
        emaR_2 = emaR[i - 2]
        emaR_yesterday = emaR[i - 1]
        emaR_today = emaR[i]
        rsi_today = rsi[i]
        is_tomorrow_green = prepared_data['Tomorrow_Green'][i]
        stock_market_signal = signal.get_signal(emaR_2, emaR_yesterday, emaR_today, rsi_today)
        t = "xanh" if is_tomorrow_green else "do"
        if stock_market_signal[0] <= 0.5:  # has sell signal
            if not is_tomorrow_green:
                total_predict_success += 1
            if is_tomorrow_green:
                total_predict_false += 1
            print("Date {} predict sell & next day is {}".format(date, t))

        if stock_market_signal[0] > 0.5:  # has buy signal
            if is_tomorrow_green:
                total_predict_success += 1
            if not is_tomorrow_green:
                total_predict_false += 1
            print("Date {} predict buy & next day is {}".format(date, t))

    print("Total success: {}".format(total_predict_success))
    print("Total false: {}".format(total_predict_false))


if __name__ == '__main__':
    ticker = "VN30F2312"
    # getting data for this generation
    date_to = "31/12/2023"
    timestamp_to = time.mktime(datetime.strptime(date_to, "%d/%m/%Y").timetuple())
    htd = stockHistory.getStockHistoryData(ticker, 1, timestamp_to)
    print("Testing VN30F2312.")

    if 'Time' in htd.columns:
        htd['DateStr'] = htd.apply(
            lambda x: datetime.fromtimestamp(x['Time']).strftime("%Y-%m-%d"), axis=1)

    htd['Today_Green'] = htd.apply(
        lambda x: True if x['Close'] >= x['Open'] else False, axis=1)

    htd["EMA_5"] = ta.ema(htd["Close"], length=5)
    htd["EMA_20"] = ta.ema(htd["Close"], length=20)
    htd['EMA_H'] = htd.apply(
        lambda x: (x['EMA_20'] - x['EMA_5']), axis=1)
    htd['EMA_R'] = htd.apply(
        lambda x: ((x['EMA_5'] - x['EMA_20']) * 10 / x['EMA_5']), axis=1)
    htd["RSI_20"] = ta.rsi(htd["Close"], length=20, fillna=True)
    htd['RSI_mini'] = htd.apply(
        lambda x: (x['RSI_20'] / 100), axis=1)
    htd['Date'] = pd.to_datetime(htd['DateStr'])
    ticker_data = htd.set_index('Date')
    prepared_data = ticker_data.drop(columns=['Time', 'DateStr', 'High', 'Low', 'Volume'])
    prepared_data['EMA_5'] = ticker_data['EMA_5'].replace(np.nan, 0)
    prepared_data['EMA_20'] = ticker_data['EMA_20'].replace(np.nan, 0)
    prepared_data['EMA_H'] = ticker_data['EMA_H'].replace(np.nan, 0)
    prepared_data['EMA_H'] = ticker_data['EMA_H'].round(0)
    prepared_data['EMA_R'] = ticker_data['EMA_R'].replace(np.nan, 0)
    prepared_data['Tomorrow_Green'] = ticker_data.Today_Green.shift(-1)
    emaR = prepared_data['EMA_R']
    rsi = prepared_data['RSI_mini']
    rows_number = len(prepared_data.index)
    signal.set_ticker("VN30")
    run()
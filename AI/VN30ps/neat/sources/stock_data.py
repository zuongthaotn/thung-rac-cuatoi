import numpy as np
import pandas_ta as ta
import pandas as pd
import time
from datetime import datetime

import vn_realtime_stock_data.stockHistory as stockHistory

def get_prepared_data(ticker):
    # getting data for this generation
    date_to = "31/10/2022"
    timestamp_to = time.mktime(datetime.strptime(date_to, "%d/%m/%Y").timetuple())
    htd = stockHistory.getStockHistoryData(ticker, 1, timestamp_to)
    if 'Time' in htd.columns:
        htd['DateStr'] = htd.apply(
            lambda x: datetime.fromtimestamp(x['Time']).strftime("%Y-%m-%d"), axis=1)

    htd['Today_Green'] = htd.apply(
        lambda x: 1 if x['Close'] >= x['Open'] else -1, axis=1)

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

    return prepared_data
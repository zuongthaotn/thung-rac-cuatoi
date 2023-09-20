import pandas as pd
import numpy as np
import pandas_ta as ta


def prepareData(htd):
    if 'Time' in htd.columns:
        from datetime import datetime

        htd['DateStr'] = htd.apply(
            lambda x: datetime.fromtimestamp(x['Time']).strftime("%Y-%m-%d"), axis=1)

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
    ticker_data.drop(['Time'], axis=1)
    ticker_data.drop(['DateStr'], axis=1)
    ticker_data['Date'] = pd.to_datetime(ticker_data.index)
    ticker_data['EMA_5'] = ticker_data['EMA_5'].replace(np.nan, 0)
    ticker_data['EMA_20'] = ticker_data['EMA_20'].replace(np.nan, 0)
    ticker_data['EMA_R'] = ticker_data['EMA_R'].replace(np.nan, 0)
    return ticker_data

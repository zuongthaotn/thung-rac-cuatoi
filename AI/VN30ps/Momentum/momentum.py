import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import numpy as np
import pandas_ta as ta
import time
import datetime

import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = [18, 12]
plt.rcParams['figure.dpi'] = 120
import seaborn as sns

import sys
import AI.constants as constants
if constants.ALGO_DIR not in sys.path:
    sys.path.insert(1, constants.ALGO_DIR)

import vn_realtime_stock_data.stockHistory as stockHistory

def prepareData(htd):
    if 'Time' in htd.columns:
        from datetime import datetime

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
    ticker_data = ticker_data.drop(columns=['Time', 'DateStr', 'High', 'Low', 'Volume'])
    ticker_data['EMA_5'] = ticker_data['EMA_5'].replace(np.nan, 0)
    ticker_data['EMA_20'] = ticker_data['EMA_20'].replace(np.nan, 0)
    ticker_data['EMA_H'] = ticker_data['EMA_H'].replace(np.nan, 0)
    ticker_data['EMA_H'] = ticker_data['EMA_H'].round(0)
    ticker_data['EMA_R'] = ticker_data['EMA_R'].replace(np.nan, 0)
    ticker_data['Tomorrow_Green'] = ticker_data.Today_Green.shift(-1)

    return ticker_data
ticker = "VN30"
date_to = "31/10/2023"
timestamp_to = time.mktime(datetime.datetime.strptime(date_to, "%d/%m/%Y").timetuple())
htd = stockHistory.getStockHistoryData(ticker, 1, timestamp_to)
prepared_data = prepareData(htd)
# print(prepared_data['EMA_H'])
# exit()

# sns.distplot(prepared_data['EMA_H'],kde=False,bins=30)
# plt.show()

# plt.scatter(prepared_data['EMA_H'], prepared_data['Tomorrow_Green'])
# plt.show()


import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import numpy as np
import pandas_ta as ta
import time
import datetime


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

    htd['Date'] = pd.to_datetime(htd['DateStr'])
    htd['Next_Close'] = htd['Close'].shift(-1)
    htd['Next_Close_Is_Up'] = htd.apply(
        lambda x: (1 if (x["Next_Close"] > x["Close"]) else 0), axis=1)

    htd['today_return'] = htd.apply(
        lambda x: (100 * (x["Close"] - x["Open"]) / (x["High"] - x["Low"])), axis=1)
    htd['today_return'] = htd['today_return'].round(2)
    htd['pass_1_return'] = htd['today_return'].shift(1)
    htd['pass_2_return'] = htd['today_return'].shift(2)

    # htd["EMA_5"] = ta.ema(htd["Close"], length=5)
    # htd["EMA_20"] = ta.ema(htd["Close"], length=20)
    # htd['EMA_H'] = htd.apply(
    #     lambda x: (x['EMA_20'] - x['EMA_5']), axis=1)
    # htd['EMA_R'] = htd.apply(
    #     lambda x: ((x['EMA_5'] - x['EMA_20']) * 10 / x['EMA_5']), axis=1)
    # htd["RSI_20"] = ta.rsi(htd["Close"], length=20, fillna=True)
    # htd['RSI_mini'] = htd.apply(
    #     lambda x: (x['RSI_20'] / 100), axis=1)
    # htd['Date'] = pd.to_datetime(htd['DateStr'])

    # ticker_data['EMA_5'] = ticker_data['EMA_5'].replace(np.nan, 0)
    # ticker_data['EMA_20'] = ticker_data['EMA_20'].replace(np.nan, 0)
    # ticker_data['EMA_H'] = ticker_data['EMA_H'].replace(np.nan, 0)
    # ticker_data['EMA_R'] = ticker_data['EMA_R'].replace(np.nan, 0)
    # ticker_data['EMA_H'] = ticker_data['EMA_H'].round(2)

    htd["RSI_5"] = ta.rsi(htd["Close"], length=5, fillna=True)
    htd["RSI_20"] = ta.rsi(htd["Close"], length=20, fillna=True)
    macd = ta.macd(htd['Close'], 20, 5, 9)
    htd = htd.assign(MACDh=macd['MACDh_5_20_9'])

    ticker_data = htd.set_index('Date')
    ticker_data.drop(columns=['Time', 'DateStr'], inplace=True)
    return ticker_data

ticker = "VN30F1M"
date_to = "31/10/2023"
timestamp_to = time.mktime(datetime.datetime.strptime(date_to, "%d/%m/%Y").timetuple())
htd = stockHistory.getStockHistoryData(ticker, 1, timestamp_to)
prepared_data = prepareData(htd)

# from pathlib import Path
# current_folder = Path(__file__).parent
# prepared_data.to_csv(str(current_folder)+'/vn30f1m.csv')
# exit()

prepared_data = prepared_data.dropna()
# print(prepared_data.shape)
# print(prepared_data[["EMA_H", "EMA_H1", "EMA_H2", "Next_Close_Up"]])
# exit()

import matplotlib.pyplot as plt


u = prepared_data.loc[prepared_data.Next_Close_Is_Up == 1]
w = prepared_data.loc[prepared_data.Next_Close_Is_Up == 0]
plt.scatter(u['today_return'], u['MACDh'], color='green')
plt.scatter(w['today_return'], w['MACDh'], color='black')
plt.show()
exit()
# print(prepared_data.loc['2023-10-27']['Open'])
# print(prepared_data.loc['2023-10-27']['Close'])
# k = prepared_data.loc[(prepared_data.EMA_H >= prepared_data.EMA_H1) & (prepared_data.EMA_H1 >= prepared_data.EMA_H2)]

# u = prepared_data.loc[(((prepared_data.pass_2_return >= prepared_data.pass_1_return) & (prepared_data.pass_1_return >= prepared_data.today_return)) | ((prepared_data.pass_2_return <= prepared_data.pass_1_return) & (prepared_data.pass_1_return <= prepared_data.today_return)))]
k = prepared_data[["pass_2_return", "pass_1_return", "today_return", "Next_Close_Is_Up"]]
X = k[["pass_1_return", "today_return"]].to_numpy()
y = k.Next_Close_Is_Up.to_numpy()
from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=2, random_state=0).fit(X)
# print('Centers found by scikit-learn:')
# print(kmeans.cluster_centers_)
pred_label = kmeans.predict(X)
print(len(pred_label))
# print(prepared_data["Next_Close_Is_Up"].to_numpy())
# print(len(prepared_data[["Next_Close_Is_Up"]].to_numpy()))
# print(pred_label == prepared_data[["Next_Close_Is_Up"]].to_numpy())
print(np.sum(pred_label == prepared_data["Next_Close_Is_Up"].to_numpy()))
# print((pred_label == prepared_data[["Next_Close_Is_Up"]].to_numpy()).sum())
exit()
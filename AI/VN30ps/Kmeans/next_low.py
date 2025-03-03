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
    htd['kDay'] = htd['Date'].dt.dayofweek
    htd['kDay'] = htd['kDay'].astype(float)
    htd['Next_Low'] = htd['Low'].shift(-1)
    htd['Next_Low_Is_Lower'] = htd.apply(
        lambda x: (1 if (x["Next_Low"] < x["Low"]) else 0), axis=1)

    htd['today_return'] = htd.apply(
        lambda x: (100 * (x["Close"] - x["Open"]) / (x["High"] - x["Low"])), axis=1)
    htd['pass_1_return'] = htd['today_return'].shift(1)
    htd['pass_2_return'] = htd['today_return'].shift(2)

    htd["EMA_5"] = ta.ema(htd["Close"], length=5)
    htd["EMA_20"] = ta.ema(htd["Close"], length=20)
    htd['EMA_H'] = htd.apply(
        lambda x: (x['EMA_20'] - x['EMA_5']), axis=1)
    htd["RSI_20"] = ta.rsi(htd["Close"], length=20)
    htd['prev_RSI_20'] = htd['RSI_20'].shift(1)
    htd['RSI_trend'] = htd.apply(
        lambda x: (x['RSI_20'] - x['prev_RSI_20']), axis=1)
    htd['RSI_trend'] = htd['RSI_trend'].round(2)
    htd['RSI_20'] = htd['RSI_20'].round(2)
    htd['EMA_H'] = htd['EMA_H'].round(2)
    htd['today_return'] = htd['today_return'].round(2)
    htd['pass_1_return'] = htd['pass_1_return'].round(2)

    ticker_data = htd.set_index('Date')
    ticker_data.drop(columns=['Time', 'DateStr'], inplace=True)
    return ticker_data


import os
from pathlib import Path
import pickle

current_folder = Path(__file__).parent
trainner_file = str(current_folder) + '/VN30F2312_next_low.pickle'
if not os.path.isfile(trainner_file):
    ticker = "VN30F1M"
    date_to = "30/04/2023"
    timestamp_to = time.mktime(datetime.datetime.strptime(date_to, "%d/%m/%Y").timetuple())
    htd = stockHistory.getStockHistoryData(ticker, 1, timestamp_to)
    prepared_data = prepareData(htd)
    prepared_data = prepared_data.dropna()
    # print(prepared_data.shape)
    # print(prepared_data)
    # exit()

    ##### ----------------- ve bieu do phan tich ---------------- ############
    # import matplotlib.pyplot as plt
    # u = prepared_data.loc[prepared_data.Next_Low_Is_Lower == 1]
    # w = prepared_data.loc[prepared_data.Next_Low_Is_Lower == 0]
    # plt.scatter(u['today_return'], u['EMA_H'], color='green')
    # plt.scatter(w['today_return'], w['EMA_H'], color='black')
    # plt.show()
    # exit()
    ##### ----------------- Endl ve bieu do phan tich ---------------- ############

    # u = prepared_data.loc[(((prepared_data.pass_2_return >= prepared_data.pass_1_return) & (prepared_data.pass_1_return >= prepared_data.today_return)) | ((prepared_data.pass_2_return <= prepared_data.pass_1_return) & (prepared_data.pass_1_return <= prepared_data.today_return)))]
    k = prepared_data[
        ["pass_2_return", "pass_1_return", "today_return", "EMA_H", "RSI_20", "RSI_trend", "Next_Low_Is_Lower"]]
    X = k[["RSI_trend", "EMA_H", "pass_1_return", "today_return"]].to_numpy()
    y = k.Next_Low_Is_Lower.to_numpy()
    from sklearn.cluster import KMeans

    kmeans = KMeans(n_clusters=2, random_state=0).fit(X)
    with open(trainner_file, 'wb') as fp:
        pickle.dump(kmeans, fp)
    # print('Centers found by scikit-learn:')
    # print(kmeans.cluster_centers_)
    # pred_label = kmeans.predict(X)
    # print('Length of data: {}' . format(len(pred_label)))
    # print('So lan du doan dung: {}' . format(np.sum(pred_label == y)))
    # exit()

else:
    # load the brain
    with open(trainner_file, 'rb') as f:
        kmeans = pickle.load(f)
    ticker = "VN30F2401"
    date_to = "31/12/2024"
    timestamp_to = time.mktime(datetime.datetime.strptime(date_to, "%d/%m/%Y").timetuple())
    htd = stockHistory.getStockHistoryData(ticker, 1, timestamp_to)
    xxx = prepareData(htd)
    xxx["Next_Low"].iloc[-1] = "-"
    xxx["Next_Low_Is_Lower"].iloc[-1] = "-"
    xxx = xxx.dropna()

    XX = xxx[["RSI_trend", "EMA_H", "pass_1_return", "today_return"]].to_numpy()
    yy = xxx.Next_Low_Is_Lower.to_numpy()

    pred_label = kmeans.predict(XX)
    print('Length of data: {}'.format(len(pred_label)))
    print('So lan du doan dung: {}'.format(np.sum(pred_label == yy)))
    slddd = np.sum(pred_label == yy)
    tlddd = (slddd / (len(pred_label) - 1)) * 100  # Ignore for predict tomorrow
    print('Ti le du doan dung: {}'.format(tlddd))

    xxx = xxx.assign(Predicts=pred_label)
    print(xxx[["Open", "Close", "High", "Low", "Next_Low_Is_Lower", "Predicts"]])
    exit()
    from pathlib import Path

    current_folder = Path(__file__).parent
    xxx.to_csv(str(current_folder) + '/' + ticker + '_next_low.csv')
    exit()

    import seaborn as sns
    import matplotlib.pyplot as plt

    # sns.displot(xxx, x="RSI_trend")

    penguins = xxx.loc[(xxx.Next_Low_Is_Lower != xxx.Predicts)]
    # print(penguins['kDay'])
    # print(penguins['RSI_trend'])
    # exit()
    # sns.displot(penguins, x="RSI_trend")
    # sns.displot(penguins, x="kDay", discrete=True)

    from pathlib import Path

    current_folder = Path(__file__).parent
    penguins.to_csv(str(current_folder) + '/VN30F2401_next_low_wrong.csv')
    exit()

    plt.show()

    exit()

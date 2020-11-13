import numpy as np
import pandas as pd
import platform
import os
import sys

BACKTESTING_MODULE_PATH = os.path.abspath('../')
sys.path.insert(1, BACKTESTING_MODULE_PATH)
import Ticker

MULTIPLIER_NUMBER = 2
DATA_PATH = os.path.abspath('../../vn-stock-data/')
if platform.system() == 'Windows':
    vnx_file = DATA_PATH + '\\VNX.csv'
if platform.system() != 'Windows':
    vnx_file = DATA_PATH + '/VNX.csv'

vnx = pd.read_csv(vnx_file, usecols=["ticker", "exchange"])
vnx_ticker = np.array(vnx)
for ticker in vnx_ticker:
    ticker_id = ticker[0]
    ticker_exchange = ticker[1]
    if ticker_exchange == 'HOSE':
        if platform.system() == 'Windows':
            file = DATA_PATH + '\\VNX\\' + ticker_id + '.csv'
        if platform.system() != 'Windows':
            file = DATA_PATH + '/VNX/' + ticker_id + '.csv'
        ticker_data = pd.read_csv(file, usecols=["Close", "Volume", "Open"])
        prices = np.array(ticker_data["Close"])
        volumes = np.array(ticker_data["Volume"])
        last_open_price = np.array(ticker_data["Open"])[-1]
        if Ticker.isFollowTrendingV2(prices, volumes, last_open_price, MULTIPLIER_NUMBER):
            last_5_volumes = volumes[-5::]
            last_3_prices = prices[-3::]
            min_volumn = min(last_5_volumes)
            max_volumn = max(last_5_volumes)
            last_volumn = last_5_volumes[-1]
            mean_f = np.mean(volumes[-5:-2])
            print(ticker_id + '--last:' + str(last_volumn) + '--mean:' + str(round(mean_f, 0)) + '--max:' + str(
                max_volumn) + '--min:' + str(min_volumn))

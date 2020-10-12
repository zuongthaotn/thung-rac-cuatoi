import numpy as np
import pandas as pd
import platform
import os

os.chdir('../')
path = os.getcwd()
if platform.system() == 'Windows':
    vnx_file = path + '\\data\\VNX.csv'
if platform.system() != 'Windows':
    vnx_file = path + '/data/VNX.csv'

vnx = pd.read_csv(vnx_file, usecols=["ticker", "exchange"])
vnx_ticker = np.array(vnx)
for ticker in vnx_ticker:
    ticker_id = ticker[0]
    ticker_exchange = ticker[1]
    if ticker_exchange == 'HOSE':
        if platform.system() == 'Windows':
            file = path + '\\cophieu68\\' + ticker_id + '.csv'
        if platform.system() != 'Windows':
            file = path + '/cophieu68/' + ticker_id + '.csv'
        ticker_data = pd.read_csv(file, usecols=["close", "volumn", "open"])
        prices = np.array(ticker_data["close"])
        volumns = np.array(ticker_data["volumn"])
        last_open_price = np.array(ticker_data["open"])[-1]
        last_5_volumns = volumns[-5::]
        last_3_prices = prices[-3::]
        min_volumn = min(last_5_volumns)
        max_volumn = max(last_5_volumns)
        last_volumn = last_5_volumns[-1]
        # if last_volumn > 2.5 * min_volumn:
        # if last_3_prices[0] < last_3_prices[1] and last_3_prices[0] < last_3_prices[2]:
        if last_3_prices[0] < last_3_prices[1] and last_3_prices[0] < last_3_prices[2] and last_volumn > 2.5 * min_volumn and last_volumn > 1000000 and last_open_price < last_3_prices[2]:
            print(ticker_id)
"""
    Exchange: HOSE
    Price: going down
    Volumn : bigger 100k
"""

import numpy as np
import pandas as pd
import platform
import os

os.chdir('../')
path = os.getcwd()
if platform.system() == 'Windows':
    vnx = pd.read_csv(path + '\\data\\VNX.csv', usecols=["ticker", "exchange"])
if platform.system() != 'Windows':
    vnx = pd.read_csv(path + '/data/VNX.csv', usecols=["ticker", "exchange"])
vnx_ticker = np.array(vnx)
total_buy = 0
total_sell = 0
for ticker in vnx_ticker:
    ticker_id = ticker[0]
    ticker_exchange = ticker[1]
    if ticker_exchange == 'HOSE':
        if platform.system() == 'Windows':
            file = path + "\\data\\VNX\\" + ticker_id + '\\Price.csv'
        if platform.system() != 'Windows':
            file = path + '/data/VNX/' + ticker_id + '/Price.csv'
        ticker_data = pd.read_csv(file, usecols=["close", "volume"])
        volume = np.array(ticker_data["volume"])
        if volume[-1] > 100000:
            price = np.array(ticker_data["close"])
            reversed_price = price[-3::]  # 3 last prices
            if reversed_price[0] > reversed_price[1] and reversed_price[1] > reversed_price[2]:
                print(ticker_id + "--" + str(reversed_price[0])+ "--" + str(reversed_price[1])+ "--" + str(reversed_price[2]))

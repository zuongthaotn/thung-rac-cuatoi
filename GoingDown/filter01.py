"""
    Only going down
"""

import numpy as np
import pandas as pd
import platform
import os

os.chdir('../')
path = os.getcwd()
if platform.system() == 'Windows':
    vnx = pd.read_csv(path + '\\data\\VNX.csv', usecols=["ticker"])
if platform.system() != 'Windows':
    vnx = pd.read_csv(path + '/data/VNX.csv', usecols=["ticker"])
vnx_ticker = np.array(vnx)
total_buy = 0
total_sell = 0
for ticker in vnx_ticker:
    ticker_id = ticker[0]
    ticker_exchange = ticker[1]
    if platform.system() == 'Windows':
        file = path + "\\data\\VNX\\" + ticker_id + '\\Price.csv'
    if platform.system() != 'Windows':
        file = path + '/data/VNX/' + ticker_id + '/Price.csv'
    ticker_data = pd.read_csv(file, usecols=["close"])
    price = np.array(ticker_data["close"])
    reversed_price = price[-4:-1]  # 3 last prices
    if reversed_price[0] > reversed_price[1] and reversed_price[1] > reversed_price[2]:
        print(ticker_id)

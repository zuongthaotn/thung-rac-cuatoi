"""
    Exchange: VN30
    Price: going down
    Volumn : bigger 100k
"""

import numpy as np
import pandas as pd
import platform
import os
import Ticker

os.chdir('../')
path = os.getcwd()
vn30_ticker = Ticker.getListVN30()
vnx_ticker = np.array(vn30_ticker)
total_buy = 0
total_sell = 0
for ticker in vnx_ticker:
    if platform.system() == 'Windows':
        file = path + "\\data\\VNX\\" + ticker + '\\Price.csv'
    if platform.system() != 'Windows':
        file = path + '/data/VNX/' + ticker + '/Price.csv'
    ticker_data = pd.read_csv(file, usecols=["close", "volume"])
    volume = np.array(ticker_data["volume"])
    if volume[-1] > 100000:
        price = np.array(ticker_data["close"])
        last_prices = price[-3::]  # 3 last prices
        if last_prices[0] > last_prices[1] and last_prices[1] > last_prices[2]:
            print(ticker + "--" + str(last_prices[0])+ "--" + str(last_prices[1])+ "--" + str(last_prices[2]))

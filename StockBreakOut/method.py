import numpy as np
import pandas as pd
import Ticker

vnx = pd.read_csv('data/VNX.csv', usecols=["ticker", "exchange"])
vnx_ticker = np.array(vnx)
total_buy = 0
total_sell = 0
for ticker in vnx_ticker:
    ticker_id = ticker[0]
    ticker_exchange = ticker[1]
    if ticker_exchange == 'HOSE':
        file = 'data/VNX/' + ticker_id + '/Price.csv'
        ticker_data = pd.read_csv(file, usecols=["close"])
        price = np.array(ticker_data["close"])
        # reversed_price = price[::-1]  # Reverse an array
        if Ticker.isStockOut(price):
            print(ticker_id)
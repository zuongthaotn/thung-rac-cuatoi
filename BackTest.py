import numpy as np
import pandas as pd
import stockOut

vnx = pd.read_csv('data/VNX.csv', usecols=["ticker", "exchange"])
vnx_ticker = np.array(vnx)
for ticker in vnx_ticker:
    ticker_id = ticker[0]
    ticker_exchange = ticker[1]
    if ticker_exchange == 'HOSE':
        file = 'data/VNX/' + ticker_id + '/Price.csv'
        ticker_data = pd.read_csv(file, usecols=["close"])
        price = np.array(ticker_data["close"])
        train_price = price.copy()
        print(train_price[::-50])
        exit()
        # test_price = price[-50::]
        # reversed_price = price[::-1]
        # if stockOut.isStockOut(reversed_price):
        #     print(ticker_id)

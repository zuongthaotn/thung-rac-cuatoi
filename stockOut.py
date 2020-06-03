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
        train_price = price[0:-10]  # get all element but ignore 50 last
        test_prices = price[-10:]  # get last 50 elements
        curr_price = price[-10]
        cut_loss_price = curr_price * 0.04
        train_price_copy = train_price.copy()
        reversed_price = train_price_copy[::-1]  # Reverse an array
        if Ticker.isStockOut(reversed_price):
            sold = False
            print("Mua co phieu "+ticker_id+" o gia: "+str(curr_price))
            total_buy += curr_price
            for test_price in test_prices:
                if test_price > curr_price:
                    cut_loss_price = test_price * 0.96
                if test_price < cut_loss_price:     # Co cut loss
                    soldPrice = test_price
                    total_sell += soldPrice
                    sold = True
                    break
                    # if test_price > curr_price:
                    #     break
                    # else:
                    #     break
            if not sold:
                soldPrice = test_price
                total_sell += soldPrice
            print("Ban co phieu " + ticker_id + " o gia: " + str(soldPrice))
            print("-----------------------------------------------------------------------------------")
if total_sell > total_buy:
    print("Lai")
else:
    print("Lo")
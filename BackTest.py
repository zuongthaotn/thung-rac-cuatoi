import numpy as np
import pandas as pd
import random
import Ticker

def main():
    ticker_id = 'CNG'
    file = 'data/VNX/' + ticker_id + '/Price.csv'
    ticker_data = pd.read_csv(file, usecols=["close"])
    price = np.array(ticker_data["close"])
    getResult(ticker_id, price)


def getResult(ticker_id, np_data):
    # rand_from = int(np_data.size / 4)
    # rand_to = int(np_data.size / 3)
    # look_back = random.randint(rand_from,rand_to) # days
    sold = False
    test_from = 100
    test_to = np_data.size - 50
    index = 0
    sold_price = 0
    commission = 0
    for price in np_data:
        index = index + 1
        if test_from < index < test_to:
            train_price = np_data[0:index]
            test_prices = np_data[index:]
            curr_price = np_data[index]
            cut_loss_price = curr_price * 0.04
            if Ticker.isStockOut(train_price):
                print("Mua co phieu " + ticker_id + " o gia: " + str(curr_price))
                for test_price in test_prices:
                    index = index + 1
                    if test_price > curr_price:
                        cut_loss_price = test_price * 0.96
                    if test_price < cut_loss_price:  # Co cut loss
                        sold_price = test_price
                        commission = sold_price - curr_price
                        sold = True
                        print("Ban co phieu " + ticker_id + " o gia: " + str(sold_price))
                        break
    print("Commission: "+str(commission))

main()

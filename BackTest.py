import numpy as np
import pandas as pd
import random
import Ticker

def main():
    ticker_id = 'CLL'
    file = 'data/VNX/' + ticker_id + '/Price.csv'
    ticker_data = pd.read_csv(file)
    data = np.array(ticker_data)
    getResult(ticker_id, data)


def getResult(ticker_id, np_data):
    # rand_from = int(np_data.size / 4)
    # rand_to = int(np_data.size / 3)
    # look_back = random.randint(rand_from,rand_to) # days
    # price_data = np_data[:, close_col_index]
    # print(price_data)
    # print(len(price_data))
    # return
    close_col_index = 4
    date_col_index = 0
    sold = False
    test_from = 100
    test_to = len(np_data) - 50
    index = 0
    sold_price = 0
    commission = 0
    train_price = np.array([])
    for data in np_data:
        index = index + 1
        train_price = np.append(train_price, data[close_col_index])
        if test_from < index < test_to:
            test_prices = np_data[index:]
            curr_price = data[close_col_index]
            cut_loss_price = curr_price * 0.04
            if Ticker.isStockOut(train_price):
                print("Mua co phieu " + ticker_id + " o gia: " + str(curr_price) + " ngay " + data[date_col_index])
                for np_test_price in test_prices:
                    test_price = np_test_price[close_col_index]
                    index = index + 1
                    if test_price > curr_price:
                        cut_loss_price = test_price * 0.96
                    if test_price < cut_loss_price:  # Co cut loss
                        sold_price = test_price
                        commission = sold_price - curr_price
                        sold = True
                        print("Ban co phieu " + ticker_id + " o gia: " + str(sold_price)+ " ngay " + np_test_price[date_col_index])
                        break
    print("Commission: "+str(commission))

main()

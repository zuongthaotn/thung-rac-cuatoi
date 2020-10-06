import numpy as np
import pandas as pd
import Ticker


def main():
    ticker_id = 'BID'
    file = '../data/VNX/' + ticker_id + '/Price.csv'
    ticker_data = pd.read_csv(file)
    data = np.array(ticker_data)
    getResult(ticker_id, data)

# Mua CP o tat ca cac diem breakout, ko quan tam CP mua truoc do da ban hay chua.
def getResult(ticker_id, np_data):
    # rand_from = int(np_data.size / 4)
    # rand_to = int(np_data.size / 3)
    # look_back = random.randint(rand_from,rand_to) # days
    # price_data = np_data[:, close_col_index]
    # print(price_data)
    # print(len(price_data))
    # return
    f = open("../tracking-history.log", "w+")
    close_col_index = 4
    date_col_index = 0
    sold = True
    test_from = 10
    test_to = len(np_data) - 5
    index = 0
    sold_price = 0
    commission = 0
    train_price = np.array([])
    for data in np_data:
        index = index + 1
        train_price = np.append(train_price, data[close_col_index])
        if test_from < index < test_to:
            copy_data = np_data.copy()
            test_prices = copy_data[index:]
            curr_price = data[close_col_index]
            cut_loss_price = curr_price * 0.96
            if Ticker.isStockOut(train_price):
                buy_log = "Mua co phieu " + ticker_id + " o gia: " + str(curr_price) + " ngay " + data[
                    date_col_index] + "\n"
                f.write(buy_log)
                # f.write("--" + str(index) + "\n")
                for np_test_price in test_prices:
                    test_price = np_test_price[close_col_index]
                    if test_price > curr_price:
                        cut_loss_price = test_price * 0.96
                    if test_price < cut_loss_price:  # Co cut loss
                        sold_price = test_price
                        commission = sold_price - curr_price
                        sold_log = "Ban co phieu " + ticker_id + " o gia: " + str(sold_price) + " ngay " + \
                                   np_test_price[date_col_index] + "\r\n"
                        f.write(sold_log)
                        # f.write("---" + str(index) + "\n")
                        break
    f.close()
    print("Commission: " + str(commission))

main()

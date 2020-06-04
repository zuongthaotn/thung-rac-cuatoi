import numpy as np
import pandas as pd
import Ticker
import CutLoss
import time

def main():
    ticker_id = 'CNG'
    file = '../data/VNX/' + ticker_id + '/Price.csv'
    ticker_data = pd.read_csv(file)
    data = np.array(ticker_data)
    getResult(ticker_id, data)

# Mua CP ở các điểm breakout, CP mua trước đó phải được bán trước khi mua tiếp.
def getResult(ticker_id, np_data):
    test_from_date = "2019-01-01"     # Y-m-d
    test_to = len(np_data) - 5
    #
    #
    f = open("../tracking-history-4.log", "w+")
    close_col_index = 4     # column closed price
    date_col_index = 0      # column date
    from_date = time.strptime(test_from_date, "%Y-%m-%d")
    index = 0
    commission = 0
    train_price = np.array([])
    jump_to = 0
    cutloss = CutLoss.byPercentage()
    for data in np_data:
        index = index + 1
        # f.write("--i: " + str(index) + "\n")
        # f.write("--j: " + str(jump_to) + "\n")
        # f.write(data[date_col_index] + "--i: " + str(index) + "--j: " + str(jump_to) + "\n")
        train_price = np.append(train_price, data[close_col_index])
        curr_date = time.strptime(data[date_col_index], "%Y-%m-%d")
        if curr_date > from_date and index > jump_to:
            if Ticker.isStockOut(train_price):
                jump_to = index     # jump to index
                copy_data = np_data.copy()
                test_prices = copy_data[index:]
                max_price = curr_price = data[close_col_index]
                cut_loss_price = curr_price * cutloss
                buy_log = "Mua co phieu " + ticker_id + " o gia: " + str(curr_price) + " ngay " + data[
                    date_col_index] + "\n"
                f.write(buy_log)
                for np_test_price in test_prices:
                    jump_to = jump_to + 1
                    test_price = np_test_price[close_col_index]
                    if test_price > max_price:
                        max_price = test_price
                        cut_loss_price = test_price * cutloss
                    # f.write(np_test_price[date_col_index] + "--price: " + str(test_price) + "--cut-loss-- " + str(cut_loss_price) + "\n")
                    if test_price < cut_loss_price:  # Co cut loss
                        sold_price = test_price
                        commission = commission + (sold_price - curr_price)
                        sold_log = "Ban co phieu " + ticker_id + " o gia: " + str(sold_price) + " ngay " + \
                                   np_test_price[date_col_index] + "\r\n"
                        f.write(sold_log)
                        break
    f.close()
    print("Commission: " + str(commission))

main()

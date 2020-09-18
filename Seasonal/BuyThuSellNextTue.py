import numpy as np
import pandas as pd
import Ticker
import platform
import os
import datetime
import time

vnx_ticker = Ticker.getListVN30()
os.chdir('../')
path = os.getcwd()
close_col_index = 4
date_col_index = 0
budget = 10000  # 10tr
test_from_date = "2020-01-01"  # Y-m-d
from_date = time.strptime(test_from_date, "%Y-%m-%d")
for ticker in vnx_ticker:
    ticker_id = ticker
    sold = True
    buy_price = 0
    commission = 0
    history_log = ''
    if platform.system() == 'Windows':
        file = path + "\\data\\VNX\\" + ticker_id + '\\Price.csv'
    if platform.system() != 'Windows':
        file = path + '/data/VNX/' + ticker_id + '/Price.csv'
    ticker_csv_data = pd.read_csv(file)
    ticker_data = np.array(ticker_csv_data)
    for data in ticker_data:
        curr_price = data[close_col_index]
        curr_date = data[date_col_index]
        curr_date_str = time.strptime(curr_date, "%Y-%m-%d")
        if curr_date_str > from_date:
            year, month, day = (int(x) for x in curr_date.split('-'))
            ans = datetime.date(year, month, day)
            # Monday is 0 and Sunday is 6.
            weekday = ans.weekday()
            if weekday == 4 and sold is True:
                sold = False
                buy_price = curr_price
                sl_buy = round(budget / (buy_price*10)) * 10
                history_log += "Mua " + str(sl_buy) + " co phieu " + ticker_id + " o gia: " + str(curr_price) + " ngay " + data[date_col_index] + "\n"
            if weekday == 2 and sold is False:
                sold = True
                commission = sl_buy * (buy_price - curr_price)
                history_log += "Ban " + str(sl_buy) + " co phieu " + ticker_id + " o gia: " + str(curr_price) + " ngay " + data[date_col_index] + "\n"
    if commission > 0 and commission > budget * 0.1:
        f = open("buy-thusday-sell-next-tuesday-" + ticker_id + ".log", "w+")
        # Don gia 1000
        print("Commission of " + ticker_id + ": " + str(round(commission * 1000, 2)))
        f.write(history_log)
        f.close()
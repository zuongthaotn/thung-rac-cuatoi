import numpy as np
import pandas as pd
import Ticker
import platform
import os
import datetime
import time
import common_vars as _v

os.chdir('../')
path = os.getcwd()
vnx = pd.read_csv('data/VNX.csv', usecols=["ticker", "exchange"])
vnx_ticker = np.array(vnx)
# vnx_ticker = Ticker.getListVN30()
close_col_index = 4
open_col_index = 1
date_col_index = 0
budget = 5000  # 5tr
test_from_date = "2020-01-01"  # Y-m-d
best_profit = 0
best_profit_ticker = ''
from_date = time.strptime(test_from_date, "%Y-%m-%d")
buyDay = _v.Monday
sellDay = _v.Thursday
for ticker in vnx_ticker:
    if ticker[1] == 'HOSE':
        ticker_id = ticker[0]
        sold = True
        buy_price = 0
        commission = 0
        maxPrice = 0
        minPrice = 0
        total_commission = 0
        time_loss = 0
        time_profit = 0
        history_log = ''
        if platform.system() == 'Windows':
            file = path + "\\data\\VNX\\" + ticker_id + '\\Price.csv'
        if platform.system() != 'Windows':
            file = path + '/data/VNX/' + ticker_id + '/Price.csv'
        ticker_csv_data = pd.read_csv(file)
        ticker_data = np.array(ticker_csv_data)
        for data in ticker_data:
            curr_date = data[date_col_index]
            curr_date_str = time.strptime(curr_date, "%Y-%m-%d")
            if curr_date_str > from_date:
                #opened_price = data[open_col_index]
                closed_price = data[close_col_index]
                if closed_price > maxPrice:
                    maxPrice = closed_price
                if minPrice == 0:
                    minPrice = closed_price
                if closed_price < minPrice:
                    minPrice = closed_price
                year, month, day = (int(x) for x in curr_date.split('-'))
                ans = datetime.date(year, month, day)
                # Monday is 0 and Sunday is 6.
                weekday = ans.weekday()
                if weekday == buyDay and sold is True:
                    sold = False
                    buy_price = closed_price
                    sl_buy = round(budget / (buy_price*10)) * 10
                    history_log += "Mua " + str(sl_buy) + " cp " + ticker_id + " gia: " + str(buy_price) + " ngay " + data[date_col_index] + "\n"
                if weekday == sellDay and sold is False:
                    history_log += "Ban " + str(sl_buy) + " cp " + ticker_id + " gia: " + str(closed_price) + " ngay " + \
                                   data[date_col_index]
                    sold = True
                    commission = sl_buy * (closed_price - buy_price)
                    total_commission += commission
                    if buy_price < closed_price:
                        time_profit += 1
                        history_log += ". Lai " + str(commission) + "\n"
                    else:
                        time_loss += 1
                        history_log += ". Lo " + str(commission) + "\n"
        if total_commission > 0 and total_commission > budget * 0.1 and time_profit > time_loss * 1.5:
            print("[" + ticker[1] + "] Total commission of " + ticker_id + ": " + str(
                round(total_commission * 1000, 2)) + ". Profits: " + str(time_profit) + ". Losses: " + str(time_loss))

        if total_commission > 0 and total_commission > budget * 0.1 and time_profit > time_loss * 1.5 and maxPrice < minPrice*1.3:
            if total_commission > best_profit:
                best_profit = total_commission
                best_profit_ticker = ticker_id
            # Don gia 1000
            print("Total commission of " + ticker_id + ": " + str(round(total_commission * 1000, 2)) + ". Profits: "+str(time_profit)+". Losses: "+str(time_loss))
            f = open('log/buyATC-sellATC-weekly/'+ticker_id + "-" + str(buyDay) + str(sellDay) + ".log", "w+")
            f.write(history_log)
            f.close()
if best_profit > 0:
    print(" Ticker's giving best profit is " + best_profit_ticker + ": " + str(round(best_profit * 1000, 2)))
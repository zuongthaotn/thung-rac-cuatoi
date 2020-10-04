import numpy as np
import os
import datetime
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import sys
sys.path.append(os.path.abspath('../'))
# import matplotlib.pyplot as plt
import common_vars as _v
from data import get_pricing
#
#
ticker_id = 'BID'
buyAndSellDays = [[0, 2], [0, 3], [0, 4],
                  [1, 3], [1, 4], [1, 0],
                  [2, 4], [2, 0], [2, 1],
                  [3, 0], [3, 1], [3, 2],
                  [4, 1], [4, 2], [4, 3]
                  ]
budget = 5000  # 5tr
start_date = '2020-01-01'
best_profit = 0
best_buy_day = -1
best_sell_day = -1
best_profit_ticker = ''
highlight = ''
commissionArr = np.array([[], [],[], [], [], [], []])
prices = get_pricing(ticker_id, start_date=start_date, fields=['close'])
ticker_data = np.array(prices)
print(ticker_data[-1])
for weekday in buyAndSellDays:
    #print("--------------------------------------"+str(_v.WEEK_DAY[weekday])+"--------------------------------------")
    sold = True
    buy_price = 0
    maxPrice = 0
    minPrice = 0
    commission = 0
    # total commisson of a weekday
    total_wd_commission = 0
    time_loss = 0
    time_profit = 0
    history_log = ''
    buyDay = weekday[0]
    sellDay = weekday[1]
    data_l = []
    for price in ticker_data:
        curr_date = price[1].strftime("%Y-%m-%d")
        closed_price = price[0]
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
            sl_buy = round(budget / (buy_price * 10)) * 10
            history_log += "Mua " + str(sl_buy) + " cp " + ticker_id + " gia: " + str(buy_price) + " ngay " + \
                           curr_date + "\n"
        if weekday == sellDay and sold is False:
            history_log += "Ban " + str(sl_buy) + " cp " + ticker_id + " gia: " + str(closed_price) + " ngay " + \
                           curr_date
            sold = True
            commission = round(sl_buy * (closed_price - buy_price), 2)
            total_wd_commission += commission
            if buy_price < closed_price:
                time_profit += 1
                history_log += ". Lai " + str(commission) + "k\n"
                data_l.append(1)
            else:
                time_loss += 1
                history_log += ". Lo " + str(commission) + "k\n"
                data_l.append(-1)
    #
    if total_wd_commission > 0 and total_wd_commission > budget * 0.1:
        if total_wd_commission > best_profit:
            best_profit = total_wd_commission
            best_profit_ticker = ticker_id
            best_buy_day = str(_v.WEEK_DAY[buyDay])
            best_sell_day = str(_v.WEEK_DAY[sellDay])
        if time_profit > time_loss * 1.5:
            highlight = '[Highlight]'
    #
    X = np.array(data_l).reshape(-1, 1)
    print(X)
    exit()
    f = open('../log/buyATC-sellATC-weekly/BlueChips/' + ticker_id + "-" + str(_v.WEEK_DAY_SHORT[buyDay]) + "-" + str(
        _v.WEEK_DAY_SHORT[sellDay]) + ".log",
             "w")
    f.write(history_log)
    f.close()
    # plt.plot(data_l)
    # plt.show()
if best_profit > 0:
    print("[Blue Chip]" + highlight + ticker_id + " giving best profit: " + str(round(best_profit * 1000, 2)) + " when buy on " + best_buy_day + " and sell on " + best_sell_day)
else:
    print("[Blue Chip]" + highlight + ticker_id + " thua lo: " + str(round(best_profit * 1000, 2)))

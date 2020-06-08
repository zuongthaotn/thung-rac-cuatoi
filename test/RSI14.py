import numpy as np
import pandas as pd

ticker_id = 'VTR'
file = '../data/VNX/' + ticker_id + '/Price.csv'
ticker_data = pd.read_csv(file)
data = np.array(ticker_data)
close_col_index = 4  # column closed price

last14days = data[-13:-1]
totalIncrease = 0
totalDecrease = 0
lastPrice = data[-14][close_col_index]
for data in last14days:
    close_price = data[close_col_index]
    if data[4] > lastPrice:
        totalIncrease = close_price - lastPrice
    else:
        totalDecrease = lastPrice - close_price
    lastPrice = close_price
RS = totalIncrease/totalIncrease
RSI = 100 - 100/(1+RS)
print(RSI)
import numpy as np
import pandas as pd

# RSI = Relative Strength Index = Chỉ số sức mạnh tương đối
ticker_id = 'VIC'
file = '../data/VNX/' + ticker_id + '/Price.csv'
ticker_data = pd.read_csv(file)
datas = np.array(ticker_data)
close_col_index = 4  # column closed price

last13days = datas[-14:-1]
totalIncrease = 0
totalDecrease = 0
lastPrice = datas[-15][close_col_index]
print(lastPrice)
for data in last13days:
    close_price = data[close_col_index]
    if close_price > lastPrice:
        totalIncrease += close_price - lastPrice
        print(close_price)
    else:
        totalDecrease += lastPrice - close_price
        print("-------"+str(close_price))
    lastPrice = close_price
print(totalIncrease)
print(totalDecrease)
RS = totalIncrease/totalDecrease
print(RS)
RSI = 100 - 100/(1+RS)
print(RSI)
# Đường RSI có thể thể hiện dự báo xu hướng tương lai của thị trường, theo 2 cách:
#
# Xu hướng tăng giá khi:  (1) Đường RSI vượt ngưỡng 50 theo hướng từ dưới lên hoặc (2) Khi đường RSI nằm ở vùng 45-55 và đường RSI vượt trên vùng 55
#
# Xu hướng giảm giá khi: (1) Đường RSI vượt ngưỡng 50 theo hướng từ trên xuống hoặc (2) Khi đường RSI ở vùng 45-55 và đường RSI vượt dưới ngưỡng 45
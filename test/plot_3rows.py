import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ticker_id = 'VTR'
file = '../data/VNX/' + ticker_id + '/Price.csv'
ticker_data = pd.read_csv(file)
data = np.array(ticker_data)

high_col_index = 2
low_col_index = 3
close_col_index = 4

close_price_data = data[:, close_col_index]
high_price_data = data[:, high_col_index]
low_price_data = data[:, low_col_index]

plt.plot(close_price_data, label='Close Price', color="black")

plt.plot(high_price_data, label='High Price', color="green")

plt.plot(low_price_data, label='Low Price', color="blue")

plt.legend(loc='best')

plt.show()

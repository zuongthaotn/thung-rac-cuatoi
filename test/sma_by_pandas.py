import pandas as pd

numbers = [1, 2, 3, 7, 9]
window_size = 3

numbers_series = pd.Series(numbers)
windows = numbers_series.rolling(window_size)
moving_averages = windows.mean()

moving_averages_list = moving_averages.tolist()
without_nans = moving_averages_list[window_size - 1:]

print(without_nans)
import os
from pathlib import Path
import pandas as pd
import pspriceaction.price_action as pa


def custom(tick):
    print(tick)
    exit()


algo_dir = Path(__file__).parent.parent
csv_file = str(algo_dir) + '/vn-stock-data/VN30ps/VN30F1M_5minutes.csv'
is_file = os.path.isfile(csv_file)
if is_file:
    dataset = pd.read_csv(csv_file, index_col='Date', parse_dates=True)
else:
    dataset = pd.read_csv(
        "https://raw.githubusercontent.com/zuongthaotn/vn-stock-data/main/VN30ps/VN30F1M_5minutes.csv",
        index_col='Date', parse_dates=True)

data = dataset.copy()
data = pa.pattern_modeling(data)
print(data[data.model != ''])
# data_len = len(data)
# print(range(data_len))
# print(data.iloc[data_len])
# for i in range(data_len):
#     print(i)
#     exit()
# data['x'] = 'safsdfdsfsfsd'
# data['high_time'] = data['x'].expanding(3).apply(custom)
# data.dropna(inplace=True)

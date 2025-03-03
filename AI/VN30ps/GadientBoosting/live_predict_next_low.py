import warnings

warnings.filterwarnings('ignore')

import pandas as pd
import time
import datetime

import vn_realtime_stock_data.stockHistory as stockHistory
import AI.VN30ps.data.get_VN30F2401 as step_one
import AI.VN30ps.data.pre_data_4_gardient_boosting as step_two

import pickle
from pathlib import Path
from sklearn import metrics

current_folder = Path(__file__).parent
trainner_file = str(current_folder) + '/GradientBoostingClassifier_next_low.pickle'
# load the brain
with open(trainner_file, 'rb') as f:
    gbc = pickle.load(f)

ticker = "VN30F2401"
date_to = "31/12/2024"
timestamp_to = time.mktime(datetime.datetime.strptime(date_to, "%d/%m/%Y").timetuple())
htd = stockHistory.getStockHistoryData(ticker, 1, timestamp_to)
# print("Total rows::", len(htd))
# exit()
htd = step_one.prepareData(htd)
prepared_data = step_two.prepareData(htd)
with pd.option_context('display.max_rows', None,
                       'display.max_columns', None,
                       'display.precision', 3,
                       ):
    print(prepared_data[["Open", "High", "Low", "Close"]].tail(2))
# split dataset in features and target variable
feature_cols = ["short_trend", "Today_Up_Down", "Volatility_ATR", "Body_Candlestick_Rate", "Tail_Candlestick_Rate",
                "Yesterday_Up_Down", "MA5_MA20", "MA5_MA20_rate", "RSI_10_Simple", "Next_Open_Is_Lower",
                "Next_Low_Is_Lower"]

prepared_data = prepared_data[feature_cols]
prepared_data.dropna(inplace=True)

X = prepared_data[feature_cols[:-1]]  # Features
y = prepared_data['Next_Low_Is_Lower']  # Target variable

pred_label = gbc.predict(X)
algo_result = prepared_data.assign(Predict_next_low=pred_label)

# with pd.option_context('display.max_rows', None,
#                        'display.max_columns', None,
#                        'display.precision', 3,
#                        ):
#     print(algo_result)

y = algo_result.Next_Low_Is_Lower.to_numpy()
print("Total rows::", len(y))
print("Accuracy:", metrics.accuracy_score(y, pred_label))
print("R2_score:", metrics.r2_score(y, pred_label))
algo_result["Next_Open_Is_Lower"].iloc[-1] = "-"
algo_result["Next_Low_Is_Lower"].iloc[-2] = "-"
algo_result["Next_Low_Is_Lower"].iloc[-1] = "-"
algo_result["Predict_next_low"].iloc[-1] = "-"
print(algo_result[["Next_Open_Is_Lower", "Predict_next_low", "Next_Low_Is_Lower"]])

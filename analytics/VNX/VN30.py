import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import numpy as np
import pandas_ta as ta
import time
import datetime

import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = [18, 12]
plt.rcParams['figure.dpi'] = 120
import seaborn as sns

import sys
import AI.constants as constants
if constants.ALGO_DIR not in sys.path:
    sys.path.insert(1, constants.ALGO_DIR)

import vn_realtime_stock_data.stockHistory as stockHistory


#@title Raw Price
def cal_open(tick):
    if not tick.empty:
        return tick[0]


def cal_high(tick):
    tick = tick[100*tick.index.hour+tick.index.minute]
    return tick.max()


def cal_low(tick):
    tick = tick[100*tick.index.hour+tick.index.minute]
    return tick.min()


def cal_price(tick):
    tick = tick[100*tick.index.hour+tick.index.minute == 1445]
    if not tick.empty:
        return tick[0]


price = stockHistory.getVN30HistoryDataByMinute()

price.volume = price.close
price = price.resample("D").agg({
    'volume': cal_open,
    'high':cal_high,
    'low': cal_low,
    'close': cal_price,
    'open': 'last',
    }).rename(columns={'volume': 'open', 'close': 'price', 'open': 'close'})

print(price)
exit()
raw = price.dropna()


import warnings

warnings.filterwarnings('ignore')

import os
import sys

METHOD_MODULE_PATH = os.path.abspath('../')
sys.path.insert(1, METHOD_MODULE_PATH)
import vn_realtime_stock_data.stockRealtimes as stockRealtime

_upf = lambda c, o, h: ((h - c) if (c > o) else (h - o))
_botf = lambda c, o, l: ((o - l) if (c > o) else (c - l))

def getMinVolumeByTime():
    from datetime import datetime
    ch = datetime.now().strftime("%H")
    cm = datetime.now().strftime("%M")
    hm = int(ch) + int(cm)/60
    return hm * 100000

import matplotlib.pyplot as plt
import numpy as np
tickers = []
bodies = []
heads = []
tails = []
data = stockRealtime.getTodayData('hose')
for ticker_data in data:
    ticker = ticker_data['stockSymbol']
    if len(ticker) != 3:
        continue
    _volume = ticker_data['nmTotalTradedQty']
    _minVol = getMinVolumeByTime()
    if type(_volume) is not int or _volume < _minVol:
        continue
    open = ticker_data['openPrice']
    ref = ticker_data['refPrice']
    close = ticker_data['matchedPrice']
    highest = ticker_data['highest']
    lowest = ticker_data['lowest']
    total_height = highest - lowest
    body = abs(close - open)
    head = _upf(close, open, highest)
    tail = _botf(close, open, lowest)
    #--------------percent-------------------#
    total_height_p = total_height / ref
    body_p = body / ref
    head_p = head / ref
    tail_p = tail / ref
    #------------------------------------------#
    tickers.append(ticker)
    heads.append(head_p)
    bodies.append(body_p)
    tails.append(tail_p)


# create data
x = tickers
y1 = np.array(bodies)
y2 = np.array(heads)
y3 = np.array(tails)

# plot bars in stack manner
plt.bar(x, y1, width=.3, color='r')
plt.bar(x, y2, width=.3, bottom=y1, color='b')
plt.bar(x, y3, width=.3, bottom=y1 + y2, color='y')
plt.xlabel("Tickers")
plt.ylabel("Percent")
plt.legend(["Body", "Head", "Tail"])
plt.title("Today ticker analytic by candlestick")
plt.show()
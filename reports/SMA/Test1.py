import warnings

warnings.filterwarnings('ignore')
# importing package
import matplotlib.pyplot as plt
import numpy as np

import os
import sys
from datetime import datetime
from datetime import date
from dateutil.relativedelta import relativedelta

METHOD_MODULE_PATH = os.path.abspath('../..')
sys.path.insert(1, METHOD_MODULE_PATH)
import vn_realtime_stock_data.stockRealtimes as stockRealtime
import vn_realtime_stock_data.stockHistory as stockHistory

_upf = lambda c, o, h: ((h - c) if (c > o) else (h - o))
_botf = lambda c, o, l: ((o - l) if (c > o) else (c - l))

vn30_ticker = ["BID", "BVH", "CTG", "FPT", "GAS", "HDB", "HPG", "KDH", "MBB", "MSN",
               "MWG", "NVL", "PDR", "PLX", "PNJ", "POW", "SSI", "STB",
               "TCB", "TPB", "VCB", "VHM", "VIC", "VJC", "VNM", "VPB", "VRE", "ACB", "SAB", "GVR"]


def getMinVolumeByTime():
    from datetime import datetime
    ch = datetime.now().strftime("%H")
    cm = datetime.now().strftime("%M")
    hm = int(ch) + int(cm) / 60
    return hm * 100000


data = stockRealtime.getTodayData('hose')
for ticker_data in data:
    ticker = ticker_data['stockSymbol']
    if len(ticker) != 3:
        continue
    _volume = ticker_data['nmTotalTradedQty']
    _minVol = getMinVolumeByTime()
    if type(_volume) is not int or _volume < _minVol:
        continue
    # if ticker not in vn30_ticker:
    #     continue
    # if ticker != 'HPG':
    #     continue

    htd = stockHistory.getStockHistoryData(ticker)  # not include today data
    # htd = jModel.convertToJapanCandle(history_ticker_data)
    if 'Time' in htd.columns:
        from datetime import datetime

        htd['Date'] = htd.apply(
            lambda x: datetime.fromtimestamp(x['Time']).strftime("%m/%d/%Y"), axis=1)
    htd['SMA_5'] = htd['Close'].rolling(window=5).mean()
    htd['SMA_20'] = htd['Close'].rolling(window=20).mean()

    # print(htd['SMA_20'])
    # print(len(htd))
    # print(htd)
    # print(range(len(htd['SMA_20'])))
    # exit()
    crossTime = 0
    lastCrossDate = ''
    for i in range(len(htd)):
        if i > 20:
            t = i-1
            if htd['SMA_5'][t] <= htd['SMA_20'][t] and htd['SMA_5'][i] >= htd['SMA_20'][i]:
                # print('_5crossingUp20...' + str(htd['Date'][i]))
                lastCrossDate = htd['Date'][i]
            # if htd['SMA_5'][i] <= htd['SMA_20'][i] and htd['SMA_5'][t] >= htd['SMA_20'][t]:
            #     print(ticker + '----' + '_5crossingDown...' + str(htd['Date'][i]))
    if lastCrossDate != '':
        crossTime = datetime.strptime(lastCrossDate + ', 14:25:00', "%m/%d/%Y, %H:%M:%S").timestamp()
    _3daysAgo = date.today() + relativedelta(days=-3)
    _3daysAgoTime = datetime.strptime(_3daysAgo.strftime("%m/%d/%Y") + ', 14:25:00', "%m/%d/%Y, %H:%M:%S").timestamp()
    if (int(crossTime) > int(_3daysAgoTime)):
        print(ticker)
    # plt.title("Line graph")
    # plt.plot(htd.SMA_5,color="red")
    # plt.plot(htd.SMA_20,color="blue")
    # plt.show()

    # previous_5 = htd['SMA_5'].shift(1)
    # previous_20 = htd['SMA_20'].shift(1)
    # _20crossingDown5 = ((htd['SMA_5'] >= htd['SMA_20']) & (previous_5 <= previous_20))  # Buy signal
    # _20crossingUp5 = ((htd['SMA_5'] <= htd['SMA_20']) & (previous_5 >= previous_20))  # Maybe sell signal
    #
    # if _20crossingDown5 is not False:
    #     try:
    #         latestDate = htd.loc[_20crossingDown5, 'Date'].iloc[0]
    #         lastTimeCrossDown = datetime.strptime(latestDate + ', 14:25:00', "%m/%d/%Y, %H:%M:%S").timestamp()
    #     except:
    #         # print("An exception occurred = " + ticker)
    #         continue
    #
    # if _20crossingUp5 is not False:
    #     try:
    #         latestUDate = htd.loc[_20crossingUp5, 'Date'].iloc[0]
    #         lastTimeCrossUp = datetime.strptime(latestUDate + ', 14:25:00', "%m/%d/%Y, %H:%M:%S").timestamp()
    #     except:
    #         # print("An exception occurred = " + ticker)
    #         continue
    #
    # if (int(lastTimeCrossDown) > int(lastTimeCrossUp)):
    #     print(ticker + '---' + str(latestUDate) + '---' + str(latestDate))
    #     print(htd.iloc[-1].Date)
    #     # plt.title("Line graph")
    #     # plt.plot(htd.SMA_5,color="red")
    #     # plt.plot(htd.SMA_20,color="blue")
    #     # plt.show()
    #     # print(htd['SMA_5'])
    #     # print(htd['SMA_20'])
    #     print(htd)
    #     exit()
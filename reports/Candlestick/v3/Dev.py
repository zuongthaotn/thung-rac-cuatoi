import warnings
warnings.filterwarnings('ignore')

from datetime import datetime

import method.JavCan as jModel
import vn_realtime_stock_data.stockRealtimes as stockRealtime
import vn_realtime_stock_data.stockHistory as stockHistory

_upf = lambda c, o, h: ((h - c) if (c > o) else (h - o))
_botf = lambda c, o, l: ((o - l) if (c > o) else (c - l))

def getMinVolumeByTime():
    ch = datetime.now().strftime("%H")
    cm = datetime.now().strftime("%M")
    hm = int(ch) + int(cm)/60
    return hm * 100000

def isCounterTrendV3b(lowPriceArrs, max_high_price_week):
    import numpy as np
    """
        Rule:
        hnay la 1 ngay tang gia
        gia mo cua nho hon 5% gia thap nhat 2 thang
        bien dong 2 thang < 40%
        20 ngay gan nhat la 1 chu ki giam gia
        
            1. Bien dong gia 3 thang(66 ngay) gan day <40%
            2. Bien dong gia 1 thang(22 ngay) gan day <20%
            3. Bien dong gia tuan(5 ngay) gan day < 15%
            4. Dang giam gia
                Price Low today is the min or smaller min5 * 3%
                Price Low today is the smaller max5 * 0.93
    :param lowPriceArrs: numpy array
    """
    week_price = lowPriceArrs[-5:-1]
    month_price = lowPriceArrs[-22:-1]
    month3s_price = lowPriceArrs[-66:-1]
    min_week = np.min(week_price)
    max_week = np.max(week_price)
    min_month = np.min(month_price)
    max_month = np.max(month_price)
    min_month3s = np.min(month3s_price)
    max_month3s = np.max(month3s_price)
    diff66 = (max_month3s - min_month3s) / max_month3s
    if diff66 > 0.41:
        return False
    diff22 = (max_month - min_month) / max_month
    if diff22 > 0.21:
        return False
    diff5 = (max_week - min_week) / max_week
    if diff5 > 0.11:
        return False
    if (week_price[-1] == min_week or week_price[-1] < min_week * 1.03\
            or week_price[-1] == min_month or week_price[-1] < min_month * 1.03\
            or week_price[-1] == min_month3s or week_price[-1] < min_month3s * 1.03)\
            and week_price[-1] < max_high_price_week * 0.93:
        return True
    return False



data = stockRealtime.getTodayData('hose')
for ticker_data in data:
    ticker = ticker_data['stockSymbol']
    if len(ticker) != 3:
        continue
    if ticker_data['highest'] == ticker_data['ceiling']:
        continue
    _volume = ticker_data['nmTotalTradedQty']
    _minVol = getMinVolumeByTime()
    if type(_volume) is not int or _volume < _minVol:
        continue
    open = ticker_data['openPrice']
    close = ticker_data['matchedPrice']
    highest = ticker_data['highest']
    lowest = ticker_data['lowest']
    total_height = highest - lowest
    body = abs(close - open)
    head = _upf(close, open, highest)
    tail = _botf(close, open, lowest)

    if open == close or open < close:
        if open == close:
            """ Today is a doji candlestick """
            ch = datetime.now().strftime("%H")
            if int(ch) < 14:
                continue
            history_ticker_data = stockHistory.getStockHistoryData(ticker)
            htd = jModel.convertToJapanCandle(history_ticker_data)
            _close = htd.Close.to_numpy()
            isDownTrend = jModel.isDownTrendV2ByRSI(_close)
            if isDownTrend is True:
                print(ticker + ' is a doji candlestick')
        else:
            print(ticker + ' is a white candlestick')
    else:
        """  Today is a black candlestick """
        continue

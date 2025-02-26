import warnings

warnings.filterwarnings('ignore')

import os
import sys
import time

METHOD_MODULE_PATH = os.path.abspath('../..')
sys.path.insert(1, METHOD_MODULE_PATH)
import method.JavCan as jModel
import vn_realtime_stock_data.stockRealtimes as stockRealtime
import vn_realtime_stock_data.stockHistory as stockHistory

_upf = lambda c, o, h: ((h - c) if (c > o) else (h - o))
_botf = lambda c, o, l: ((o - l) if (c > o) else (c - l))

# Open a file with access mode 'a'
file_object = open('sample.txt', 'a')

data = stockRealtime.getTodayData('hose')
for ticker_data in data:
    ticker = ticker_data['stockSymbol']
    if len(ticker) != 3:
        continue
    _volume = ticker_data['nmTotalTradedQty']
    if type(_volume) is not int or _volume < 500000:
        continue
    # _open = ticker_data['openPrice']
    # _close = ticker_data['matchedPrice']
    # _highest = ticker_data['highest']
    # _lowest = ticker_data['lowest']
    # _height = _highest - _lowest
    # _body = abs(_close - _open)
    # _up = _upf(_close, _open, _highest)
    # _bot = _botf(_close, _open, _lowest)

    condition = jModel.isWhiteCandlestick(ticker_data['openPrice'], ticker_data['matchedPrice'])
    # today is a white candlestick
    if condition is True:
        # print(ticker)
        history_ticker_data = stockHistory.getStockHistoryData(ticker)  # not include today data
        # print(history_ticker_data)
        htd = jModel.convertToJapanCandle(history_ticker_data)
        _open = htd.Open.to_numpy()
        _close = htd.Close.to_numpy()
        _highest = htd.High.to_numpy()
        _lowest = htd.Low.to_numpy()
        _height = htd.Height.to_numpy()
        _body = htd.Body.to_numpy()
        _up = htd.UpShadow.to_numpy()
        _bot = htd.LowerShadow.to_numpy()
        # isDownTrend = jModel.isDownTrendV1(_open, _close, _highest, _lowest, _body, _height, _up, _bot)
        isDownTrend = jModel.isDownTrendV2ByRSI(_close)
        _iuc = jModel.isHammer(_body[-1], _height[-1], _up[-1], _bot[-1])

        if isDownTrend is True:
            if _iuc is True:
                print(ticker)
                file_object.write(ticker + '---Buy---\n')
            else:
                # Append 'hello' at the end of file
                file_object.write(ticker + '---None---\n')
                # Close the file
        time.sleep(2)
file_object.close()
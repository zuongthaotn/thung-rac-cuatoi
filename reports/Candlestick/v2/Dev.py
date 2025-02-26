import warnings
warnings.filterwarnings('ignore')

from datetime import datetime

import os
import sys

METHOD_MODULE_PATH = os.path.abspath('.')
sys.path.insert(1, METHOD_MODULE_PATH)

import method.JavCan as jModel
import vn_realtime_stock_data.stockRealtimes as stockRealtime
import vn_realtime_stock_data.stockHistory as stockHistory

_upf = lambda c, o, h: ((h - c) if (c > o) else (h - o))
_botf = lambda c, o, l: ((o - l) if (c > o) else (c - l))

def getMinVolumeByTime():
    ch = datetime.now().strftime("%H")
    cm = datetime.now().strftime("%M")
    hm = int(ch) + int(cm) / 60
    return hm * 100000

for exchange in ['hose', 'hnx', 'upcom']:
    data = stockRealtime.getTodayData(exchange)
    selectedTickers = []
    message = 'Những cổ phiếu đc xem xét: \n'
    for ticker_data in data:
        ticker = ticker_data['stockSymbol']
        if len(ticker) != 3:
            continue
        if ticker_data['highest'] == ticker_data['ceiling']:
            continue
        if ticker_data['matchedPrice'] == ticker_data['floor']:
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
        price = close/1000
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
                selectedTickers.append(ticker)
                message += ticker + "(" + str(price)+")\n"
        elif open < close:
            """ Today is a white candlestick """
            go_pass = False
            # ----------------------------------------------------------------------------------------------
            isHammer = jModel.isHammer(body, total_height, head, tail)
            isSpinningTopCandlestick = jModel.isSpinningTopCandlestick(body, total_height, head, tail)
            isShavenHead = jModel.isShavenHead(total_height, head)
            isShavenBottom = jModel.isShavenBottom(total_height, tail)
            isBigBody = jModel.isBigBody(body, total_height, open, close)
            isLongTail = True if tail > 0.65 * total_height else False
            # ----------------------------------------------------------------------------------------------
            if isBigBody is True:
                if isShavenHead is True or isShavenBottom is True:
                    go_pass = True
            else:
                if isLongTail is True:
                    if total_height > 0.05 * close:
                        """ Oscillation amplitude must be bigger than 5%"""
                        go_pass = True
                if isSpinningTopCandlestick is True:
                    ch = datetime.now().strftime("%H")
                    if int(ch) < 14:
                        continue
                    go_pass = True
            # ----------------------------------------------------------------------------------------------
            if go_pass:
                print(ticker + '--is--passed--a--simple-checking--list------')
                history_ticker_data = stockHistory.getStockHistoryData(ticker)  # not include today data
                htd = jModel.convertToJapanCandle(history_ticker_data)
                _close = htd.Close.to_numpy()
                isDownTrend = jModel.isDownTrendV2ByRSI(_close)
                if isDownTrend is True:
                    selectedTickers.append(ticker)
                    message += ticker + "(" + str(price) + ")\n"
            # ----------------------------------------------------------------------------------------------
        else:
            """  Today is a black candlestick """
            continue

if selectedTickers:
    print(message)

# print(ticker + '--is--added--to--checking--list------')
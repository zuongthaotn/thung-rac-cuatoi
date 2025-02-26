import warnings

warnings.filterwarnings('ignore')

import os
import sys

METHOD_MODULE_PATH = os.path.abspath('.')
sys.path.insert(1, METHOD_MODULE_PATH)
import vn_realtime_stock_data.stockRealtimes as stockRealtime
import vn_realtime_stock_data.stockHistory as stockHistory
import method.MACD.v1 as v1

import gsheet.service as gSheetService
sheet_data = gSheetService.get_data("1roOZQvWo4g_M6uZj6t-3jriELM_pmkizt7b4k9Ni2VQ", "A1:D")
buy_list = sheet_data.Ticker.values.tolist()


selectedTickers = []
message = 'Những cổ phiếu đc xem xét(Bán): \n'
ticker_log = ''
for exchange in ['hose', 'hnx', 'upcom']:
    data = stockRealtime.getTodayData(exchange)
    for ticker_data in data:
        ticker = ticker_data['stockSymbol']
        if len(ticker) != 3:
            continue
        _volume = ticker_data['nmTotalTradedQty']
        if type(_volume) is not int:
            continue
        if ticker not in buy_list:
            continue

        _open = ticker_data['openPrice']
        _close = ticker_data['matchedPrice']
        _price = _close / 1000

        htd = stockHistory.getStockHistoryData(ticker)  # not include today data
        prepared_data = v1.prepareData(htd)

        ticker_log += ticker + "-" + str(_close) + " "
        if v1.hasSellSignal(prepared_data['MACD'], prepared_data['MACDs']):
            selectedTickers.append(ticker)
            message += ticker + "(" + str(_price) + ")\n"
if selectedTickers:
    print(message)
print(ticker_log)
print("Done!")
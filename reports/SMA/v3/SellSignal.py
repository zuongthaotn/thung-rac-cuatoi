import warnings

warnings.filterwarnings('ignore')

import os
import sys

METHOD_MODULE_PATH = os.path.abspath('.')
sys.path.insert(1, METHOD_MODULE_PATH)
import vn_realtime_stock_data.stockRealtimes as stockRealtime
import vn_realtime_stock_data.stockHistory as stockHistory
import method.SMA.v3 as v3

import gsheet.service as gSheetService
sheet_data = gSheetService.get_data("1roOZQvWo4g_M6uZj6t-3jriELM_pmkizt7b4k9Ni2VQ", "A1:D")
buy_list = sheet_data.Ticker.values.tolist()


selectedTickers = []
message = 'Những cổ phiếu đc xem xét(Bán): \n'
data = stockRealtime.getTodayData('hose')
ticker_log = ''
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
    prepared_data = v3.prepareData(htd)

    open = prepared_data['Open'].to_numpy()
    close = prepared_data['Close'].to_numpy()
    sma_h = prepared_data['SMA_H'].to_numpy()
    sma5 = prepared_data['SMA_5'].to_numpy()
    sma20 = prepared_data['SMA_20'].to_numpy()

    ticker_log += ticker + "-" + str(_close) + " "
    if v3.hasSellSignal(open, close, sma_h, sma5, sma20, cutoff_percent=0.99):
        selectedTickers.append(ticker)
        message += ticker + "(" + str(_price) + ")\n"
if selectedTickers:
    print(message)
print(ticker_log)
print("Done!")
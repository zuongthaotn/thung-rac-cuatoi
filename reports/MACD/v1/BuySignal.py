import warnings

warnings.filterwarnings('ignore')
import sys
import sys_path

sys.path.insert(1, sys_path.METHOD_MODULE_PATH)
import vn_realtime_stock_data.stockRealtimes as stockRealtime
import vn_realtime_stock_data.stockHistory as stockHistory
import method.MACD.v1 as v1

best_sharpe_ratio = ["ACB", "ANV", "BCG", "DCM", "DGW", "DIG", "DLG", "EVF", "FPT", "FTS", "GMD", "HAX", "HCM", "IBC",
                     "IJC", "KDH", "KPF", "MBB", "MSB", "NKG", "NLG", "OCB", "SCR", "SSI", "SZC", "VCB", "VCI", "VGC",
                     "VIB", "AAV", "MBS", "TNG", "TVC", "VFS", "AAS", "ABB", "ABW"]




selectedTickers = []
message = '(MACD.v1)Những cổ phiếu đc xem xét(MUA): \n'
for exchange in ['hose', 'hnx', 'upcom']:
    data = stockRealtime.getTodayData(exchange)
    for ticker_data in data:
        ticker = ticker_data['stockSymbol']
        if len(ticker) != 3:
            continue
        _volume = ticker_data['nmTotalTradedQty']
        if type(_volume) is not int:
            continue
        if ticker not in best_sharpe_ratio:
            continue

        close = ticker_data['matchedPrice']
        price = close / 1000

        htd = stockHistory.getStockHistoryData(ticker)
        prepared_data = v1.prepareData(htd)
        if v1.hasBuySignal(prepared_data['MACD'], prepared_data['MACDs']):
            selectedTickers.append(ticker)
            message += ticker + "(" + str(price) + ")\n"

if selectedTickers:
    print(message)
print("Done!")

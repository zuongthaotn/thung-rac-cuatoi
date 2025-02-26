#
import vn_realtime_stock_data.stockHistory as stockHistory
import method.JavCan as jModel
#
ticker = 'ACB'
history_ticker_data = stockHistory.getStockHistoryData(ticker)
htd = jModel.convertToJapanCandle(history_ticker_data)
_close = htd.Close.to_numpy()
isDownTrend = jModel.isDownTrendV2ByRSI(_close)
print(isDownTrend)
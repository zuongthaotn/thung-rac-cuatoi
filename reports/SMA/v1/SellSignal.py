import warnings

warnings.filterwarnings('ignore')

import os
import sys
from datetime import datetime
from datetime import date
from dateutil.relativedelta import relativedelta

METHOD_MODULE_PATH = os.path.abspath('.')
sys.path.insert(1, METHOD_MODULE_PATH)
import vn_realtime_stock_data.stockRealtimes as stockRealtime
import vn_realtime_stock_data.stockHistory as stockHistory

_upf = lambda c, o, h: ((h - c) if (c > o) else (h - o))
_botf = lambda c, o, l: ((o - l) if (c > o) else (c - l))

love_list = ["SCR", "TCH", "NVL", "DIG", "DXG", "PDR", "HPX", "HCM", "CII", "HT1", "VHM", "VGC", "VND", "SAM", "ASM",
             "CTD", "SSI", "VCI", "BCG", "SHB", "BID", "HPG", "SZC", "HSG", "STB", "AAA", "ACB", "DXS", "HBC", "NLG",
             "VRE", "GVR", "DGC", "MBB", "OCB", "PC1", "SAB", "GEX", "NKG", "PAN", "CRE", "DHC", "LPB", "IMP", "VIC",
             "CTG", "DCM", "MSB", "PTB", "VPB", "HDG", "REE", "BVH", "DBC", "FPT", "GEG", "PHR", "PLX", "TPB", "ANV",
             "CTR", "HNG", "MSN", "SJS", "VNM", "GMD", "KOS", "POW", "VCB", "BMP", "KDH", "PVD", "VCG", "VIB", "PVT",
             "SSB", "GAS", "TCB", "HDB", "SBT", "CMG", "DGW", "VSH", "BCM", "EIB", "PPC", "SCS", "VHC", "FRT", "BWE",
             "KBC", "PNJ", "VPI", "NT2", "VJC", "MWG", "AGG", "DPM", "KDC", "TMS", "BSR"]


selectedTickers = []
message = 'Những cổ phiếu đc xem xét(Bán): \n'
data = stockRealtime.getTodayData('hose')
for ticker_data in data:
    ticker = ticker_data['stockSymbol']
    if len(ticker) != 3:
        continue
    _volume = ticker_data['nmTotalTradedQty']
    if type(_volume) is not int:
        continue
    if ticker not in love_list:
        continue

    close = ticker_data['matchedPrice']
    price = close / 1000

    htd = stockHistory.getStockHistoryData(ticker)  # not include today data
    if 'Time' in htd.columns:
        from datetime import datetime

        htd['Date'] = htd.apply(
            lambda x: datetime.fromtimestamp(x['Time']).strftime("%m/%d/%Y"), axis=1)
    htd['SMA_5'] = htd['Close'].rolling(window=5).mean()
    htd['SMA_20'] = htd['Close'].rolling(window=20).mean()
    l = htd['SMA_5'].size
    if htd['SMA_20'][l - 1] < htd['SMA_5'][l - 1] and price < htd['SMA_5'][l - 1]:
        selectedTickers.append(ticker)
        message += ticker + "(" + str(price) + ")\n"
if selectedTickers:
    sendTelegramMessage(message)

import os
import sys
import warnings
warnings.filterwarnings('ignore')

import sys_path
sys.path.insert(1, sys_path.METHOD_MODULE_PATH)
import vn_realtime_stock_data.stockRealtimes as stockRealtime
import vn_realtime_stock_data.stockHistory as stockHistory
import method.SMA.v3 as v3

love_list = ["SCR", "TCH", "NVL", "DIG", "DXG", "PDR", "HPX", "HCM", "CII", "HT1", "VHM", "VGC", "VND", "SAM", "ASM",
             "CTD", "SSI", "VCI", "BCG", "SHB", "BID", "HPG", "SZC", "HSG", "STB", "AAA", "ACB", "DXS", "HBC", "NLG",
             "VRE", "GVR", "DGC", "MBB", "OCB", "PC1", "SAB", "GEX", "NKG", "PAN", "CRE", "DHC", "LPB", "IMP", "VIC",
             "CTG", "DCM", "MSB", "PTB", "VPB", "HDG", "REE", "BVH", "DBC", "FPT", "GEG", "PHR", "PLX", "TPB", "ANV",
             "CTR", "HNG", "MSN", "SJS", "VNM", "GMD", "KOS", "POW", "VCB", "BMP", "KDH", "PVD", "VCG", "VIB", "PVT",
             "SSB", "GAS", "TCB", "HDB", "SBT", "CMG", "DGW", "VSH", "BCM", "EIB", "PPC", "SCS", "VHC", "FRT", "BWE",
             "KBC", "PNJ", "VPI", "NT2", "VJC", "MWG", "AGG", "DPM", "KDC", "TMS", "BSR"]

best_sharpe_ratio = ["ABS", "SSB", "DIG", "ITA", "DPG", "CTS", "APG", "MHC", "TDC", "ANV", "SSI", "GMD", "TCH", "DAH", "FCN",
             "PHC", "ASM", "NTL", "ADS", "VIX", "QCG", "NLG", "TSC", "PC1", "ITC", "LSS", "HDB", "TPB", "FIT", "QBS",
             "GEX", "DLG", "OCB", "FTS", "DPM", "TTF", "PVT", "ORS", "MSB", "GEG", "VPB", "HTN", "NKG", "LCG", "MWG",
             "HQC", "SCR", "IDI", "PTL", "KBC", "TCD", "APH", "VCB", "HCM", "HHS", "MBB", "VCI", "DGW"]


selectedTickers = []
message = '(SMA.v3)Những cổ phiếu đc xem xét(MUA): \n'
data = stockRealtime.getTodayData('hose')
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
    prepared_data = v3.prepareData(htd)
    sma_h = prepared_data['SMA_H'].to_numpy()
    if v3.hasBuySignal(sma_h):
        selectedTickers.append(ticker)
        message += ticker + "(" + str(price) + ")\n"

if selectedTickers:
    sendTelegramMessage(message)
print("Done!")

import sys
import sys_path
import warnings
warnings.filterwarnings('ignore')

from datetime import datetime
from datetime import date
from dateutil.relativedelta import relativedelta

sys.path.insert(1, sys_path.BACKTESTING_MODULE_PATH)
from backtesting.backtesting import Backtest, Strategy
from backtesting.test import SMA
import vn_realtime_stock_data.stockHistory as stockHistory
import method.MACD.v1 as v1


def RSI(array, n):
    import pandas as pd
    """Relative strength index"""
    # Approximate; good enough
    gain = pd.Series(array).diff()
    loss = gain.copy()
    gain[gain < 0] = 0
    loss[loss > 0] = 0
    rs = gain.ewm(n).mean() / loss.abs().ewm(n).mean()
    return 100 - 100 / (1 + rs)

class Macd(Strategy):
    def init(self):
        self.buy_price = 0
        self.current_price = 0
        self.peak_price = 0
        price = self.data.Close
        # self.close = self.I(lambda: (price))
        self.ma5 = self.I(SMA, price, 5)
        self.ma20 = self.I(SMA, price, 20)
        self.ma60 = self.I(SMA, price, 60)
        self.macd = self.data.MACD
        self.signal = self.data.MACDs
        self.draw = self.I(lambda: (self.macd, self.signal), name='macd', overlay=False)
        self.draw_h = self.I(lambda: (self.data.MACDh), name='MACDh', overlay=False)
        # Compute daily RSI(30)
        self.daily_rsi = self.I(RSI, self.data.Close, 22)

    def next(self):
        self.current_price = self.data.Close[-1]
        today_open = self.data.Open[-1]
        if self.buy_price == 0 and v1.hasBuySignal(self.data.MACD, self.data.MACDs):
            self.buy()
            self.buy_price = self.data.Close[-1]
            self.peak_price = self.data.Close[-1]
        elif self.buy_price != 0:
            if self.peak_price < self.data.Close[-1]:
                self.peak_price = self.data.Close[-1]
            if v1.hasSellSignal02(today_open, self.current_price, self.peak_price, self.data.MA_5[-1]):
                self.position.close()
                self.buy_price = 0
                self.peak_price = 0

import random
love_list = ["SCR", "TCH", "NVL", "DIG", "DXG", "PDR", "HPX", "HCM", "CII", "HT1", "VHM", "VGC", "VND", "SAM", "ASM",
             "CTD", "SSI", "VCI", "BCG", "SHB", "BID", "HPG", "SZC", "HSG", "STB", "AAA", "ACB", "DXS", "HBC", "NLG",
             "VRE", "GVR", "DGC", "MBB", "OCB", "PC1", "SAB", "GEX", "NKG", "PAN", "CRE", "DHC", "LPB", "IMP", "VIC",
             "CTG", "DCM", "MSB", "PTB", "VPB", "HDG", "REE", "BVH", "DBC", "FPT", "GEG", "PHR", "PLX", "TPB", "ANV",
             "CTR", "HNG", "MSN", "SJS", "VNM", "GMD", "KOS", "POW", "VCB", "BMP", "KDH", "PVD", "VCG", "VIB", "PVT",
             "SSB", "GAS", "TCB", "HDB", "SBT", "CMG", "DGW", "VSH", "BCM", "EIB", "PPC", "SCS", "VHC", "FRT", "BWE",
             "KBC", "PNJ", "VPI", "NT2", "VJC", "MWG", "AGG", "DPM", "KDC", "TMS", "BSR"]

ticker_id = random.choice(love_list)
ticker_id = 'MBB'
two_years = date.today() + relativedelta(years=-2)
timestamp_from = datetime.strptime(two_years.strftime("%m/%d/%Y") + ', 00:00:0', "%m/%d/%Y, %H:%M:%S").timestamp()
timestamp_to = datetime.strptime(date.today().strftime("%m/%d/%Y") + ', 23:59:00', "%m/%d/%Y, %H:%M:%S").timestamp()
htd = stockHistory.getStockHistoryData(ticker_id, timestamp_from, timestamp_to)
prepared_data = v1.prepareData(htd)
bt = Backtest(prepared_data, Macd)
stats = bt.run()
print(stats)
bt.plot()
# print(optimized_stats)
# print(optimized_stats._strategy)
print(ticker_id)
# path = os.getcwd()
# new_file = path+"/result_"+ticker_id+"_2.csv"
# stats['_trades'].to_csv(new_file, index=False)
# print(profit)

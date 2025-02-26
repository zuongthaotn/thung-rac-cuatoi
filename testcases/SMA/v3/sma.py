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
import method.SMA.v3 as v3

profit = 0
class Sma(Strategy):
    cutoff_percent = 0.99
    d = 0
    def init(self):
        price = self.data.Close
        self.buy_price = 0
        self.ma5 = self.I(SMA, price, 5)
        self.ma20 = self.I(SMA, price, 20)

    def next(self):
        global profit
        if (len(self.data.SMA_H) < 21):
            return
        close_price = self.data.Close[-1]
        self.d = self.d + 1
        if self.buy_price == 0 and v3.hasBuySignal(self.data.SMA_H):
            self.buy()
            self.buy_price = self.data.Close[-1]
            self.d = 0
        elif self.buy_price != 0 and v3.hasSellSignal(self.data.Open, self.data.Close, self.data.SMA_H, self.data.SMA_5,self.data.SMA_20, cutoff_percent=self.cutoff_percent) and self.d > 2:
            self.position.close()
            profit += (self.data.Close[-1] - self.buy_price)
            # print("Bought price: " +str(self.buy_price) + ' - Sold price: ' + str(self.data.Close[-1]))
            self.buy_price = 0


import random
love_list = ["SCR", "TCH", "NVL", "DIG", "DXG", "PDR", "HPX", "HCM", "CII", "HT1", "VHM", "VGC", "VND", "SAM", "ASM",
             "CTD", "SSI", "VCI", "BCG", "SHB", "BID", "HPG", "SZC", "HSG", "STB", "AAA", "ACB", "DXS", "HBC", "NLG",
             "VRE", "GVR", "DGC", "MBB", "OCB", "PC1", "SAB", "GEX", "NKG", "PAN", "CRE", "DHC", "LPB", "IMP", "VIC",
             "CTG", "DCM", "MSB", "PTB", "VPB", "HDG", "REE", "BVH", "DBC", "FPT", "GEG", "PHR", "PLX", "TPB", "ANV",
             "CTR", "HNG", "MSN", "SJS", "VNM", "GMD", "KOS", "POW", "VCB", "BMP", "KDH", "PVD", "VCG", "VIB", "PVT",
             "SSB", "GAS", "TCB", "HDB", "SBT", "CMG", "DGW", "VSH", "BCM", "EIB", "PPC", "SCS", "VHC", "FRT", "BWE",
             "KBC", "PNJ", "VPI", "NT2", "VJC", "MWG", "AGG", "DPM", "KDC", "TMS", "BSR"]

ticker_id = random.choice(love_list)
ticker_id = 'GEG'
two_years = date.today() + relativedelta(years=-2)
timestamp_from = datetime.strptime(two_years.strftime("%m/%d/%Y") + ', 00:00:0', "%m/%d/%Y, %H:%M:%S").timestamp()
timestamp_to = datetime.strptime(date.today().strftime("%m/%d/%Y") + ', 23:59:00', "%m/%d/%Y, %H:%M:%S").timestamp()
htd = stockHistory.getStockHistoryData(ticker_id, timestamp_from, timestamp_to)
prepared_data = v3.prepareData(htd)
bt = Backtest(prepared_data, Sma)
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

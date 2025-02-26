import warnings
warnings.filterwarnings('ignore')

import os
import sys

import method.algofuncs as _af
import pandas as pd

BACKTESTING_MODULE_PATH = os.path.abspath('backtest')
sys.path.insert(1, BACKTESTING_MODULE_PATH)
from backtesting.backtesting import Backtest, Strategy
from backtesting.test import SMA
import method.SMA.v4 as v4
import method.SMA.v3 as v3

profit = 0
class Sma02(Strategy):
    cutoff_percent = 0.99
    def init(self):
        price = self.data.Close
        self.buy_price = 0
        self.ma5 = self.I(SMA, price, 5)
        self.ma20 = self.I(SMA, price, 20)
        # self.c_price_rsi = self.I(v4.RSI, self.data.Close, 10)
        # self.volumn_rsi = self.I(v4.RSI, self.data.Volume, 10)

    def next(self):
        global profit
        if (len(self.data.SMA_H) < 21):
            return
        # if self.buy_price == 0 and v3.hasBuySignal(self.data.SMA_H):
        if self.buy_price == 0 and v4.hasBuySignal(self.data.SMA_H, open=self.data.Open, close=self.data.Close, sma5=self.data.SMA_5):
            self.buy()
            self.buy_price = self.data.Close[-1]
        # elif self.buy_price != 0 and v3.hasSellSignal(self.data.Open, self.data.Close, self.data.SMA_H, self.data.SMA_5, self.data.SMA_20, cutoff_percent=self.cutoff_percent):
        elif self.buy_price != 0 and v4.hasSellSignal(self.data.Open, self.data.Close, self.data.SMA_H, self.data.SMA_5, self.data.SMA_20, cutoff_percent=self.cutoff_percent):
            self.position.close()
            profit += (self.data.Close[-1] - self.buy_price)
            # print("Bought price: " +str(self.buy_price) + ' - Sold price: ' + str(self.data.Close[-1]))
            self.buy_price = 0


DATA_PATH = os.path.abspath('vn-stock-data/VNX/')

import random
love_list = ["SCR", "TCH", "NVL", "DIG", "DXG", "PDR", "HPX", "HCM", "CII", "HT1", "VHM", "VGC", "VND", "SAM", "ASM",
             "CTD", "SSI", "VCI", "BCG", "SHB", "BID", "HPG", "SZC", "HSG", "STB", "AAA", "ACB", "DXS", "HBC", "NLG",
             "VRE", "GVR", "DGC", "MBB", "OCB", "PC1", "SAB", "GEX", "NKG", "PAN", "CRE", "DHC", "LPB", "IMP", "VIC",
             "CTG", "DCM", "MSB", "PTB", "VPB", "HDG", "REE", "BVH", "DBC", "FPT", "GEG", "PHR", "PLX", "TPB", "ANV",
             "CTR", "HNG", "MSN", "SJS", "VNM", "GMD", "KOS", "POW", "VCB", "BMP", "KDH", "PVD", "VCG", "VIB", "PVT",
             "SSB", "GAS", "TCB", "HDB", "SBT", "CMG", "DGW", "VSH", "BCM", "EIB", "PPC", "SCS", "VHC", "FRT", "BWE",
             "KBC", "PNJ", "VPI", "NT2", "VJC", "MWG", "AGG", "DPM", "KDC", "TMS", "BSR"]

ticker_id = random.choice(love_list)
ticker_id = 'ACB'
ticker_data = _af.get_pricing_by_path(DATA_PATH + '/' + ticker_id + '.csv', '2018-01-01', '2022-12-30')
prepared_data = v4.prepareDataVersionOffline(ticker_data)
# pd.set_option('max_columns', None)
# print(prepared_data)
# exit()
bt = Backtest(prepared_data, Sma02)
stats = bt.run()
print(stats)
print("-----------------------------------------------------------------------------------------------------------------------------")
# optimized_stats = bt.optimize(cutoff_percent=(0.89, 0.9, 0.91, 0.92, 0.93, 0.94, 0.95, 0.96, 0.97, 0.98, 0.99))
bt.plot()
# print(optimized_stats)
# print(optimized_stats._strategy)
print(ticker_id)
# print(profit)

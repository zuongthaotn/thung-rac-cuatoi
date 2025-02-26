import warnings

warnings.filterwarnings('ignore')

import os
import sys
import pandas as pd
import numpy as np

METHOD_MODULE_PATH = os.path.abspath('../..')
sys.path.insert(1, METHOD_MODULE_PATH)
import method.algofuncs as _af
import method.JavCan as jModel

DATA_PATH = os.path.abspath('../../vn-stock-data/VNX/')
vn30_ticker = _af.getListVN30()
# vnx_file = os.path.abspath('../../vn-stock-data/VNX.csv')
# hose_ticker = _af.getHOSETickers(vnx_file)
# for ticker_id in all_ticker:

DATA_PATH = os.path.abspath('../../vn-stock-data/VNX/')
hold_tickers = ['ABB', 'ACB', 'BSR', 'FPT', 'GMD', 'OCB', 'PVS', 'PVT', 'STB', 'TPB', 'VCI', 'VHG', 'VND', 'VGT']
printedDate = False
for ticker_id in hold_tickers:
    ticker_data = _af.get_pricing_by_path(DATA_PATH + '/' + ticker_id + '.csv', '2021-07-01')
    if printedDate == False:
        print(ticker_data.Date[-1])
        printedDate = True
    _1hit_data = ticker_data.tail(10)
    new_data = jModel.convertToJapanCandle(_1hit_data)

    hasSellSignal = jModel.hasSellSignal(new_data.Open, new_data.Close, new_data.High, new_data.Low,
                                       new_data.Body, new_data.Height, new_data.UpShadow,
                                       new_data.LowerShadow, new_data.Date)

    if hasSellSignal is not False:
        print(ticker_id + ' -- ' + str(hasSellSignal))

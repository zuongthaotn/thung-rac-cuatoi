import warnings

warnings.filterwarnings('ignore')

import os
import sys

METHOD_MODULE_PATH = os.path.abspath('../..')
sys.path.insert(1, METHOD_MODULE_PATH)
import method.algofuncs as _af
import method.JavCan as jModel

DATA_PATH = os.path.abspath('../../vn-stock-data/VNX/')
hold_tickers = ['ABB', 'ACB', 'BSR', 'FPT', 'GMD', 'OCB', 'PVS', 'PVT', 'STB', 'TPB', 'VCI', 'VHG', 'VND', 'VGT']
printedDate = False
for ticker_id2 in hold_tickers:
    ticker_data = _af.get_pricing_by_path(DATA_PATH + '/' + ticker_id2 + '.csv', '2021-05-01')
    if printedDate == False:
        print(ticker_data.Date[-1])
        printedDate = True
    _1hit_data = ticker_data.tail(10)
    new_data = jModel.convertToJapanCandle(_1hit_data)
    hasSellSignal = jModel.hasCustomSellSignal(new_data.Open, new_data.Close, new_data.High, new_data.Low,
                                         new_data.Body, new_data.Height, new_data.UpShadow,
                                         new_data.LowerShadow, new_data.Date)
    if hasSellSignal is not False:
        print(ticker_id2 + ' -- ' + str(hasSellSignal))
        # print(jModel.isBlackCandlestick(new_data.Open[-3], new_data.Close[-3]))
        # print(jModel.isBlackCandlestick(new_data.Open[-2], new_data.Close[-2]))
        # print(jModel.isBlackCandlestick(new_data.Open[-1], new_data.Close[-1]))
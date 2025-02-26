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

vnx_file = os.path.abspath('../../vn-stock-data/Tickers.csv')
all_ticker = pd.read_csv(vnx_file, usecols=["ticker"])
for index, ticker_id in all_ticker.ticker.iteritems():
    if ticker_id == 'ticker' or ticker_id == '':
        continue
    ticker_data = _af.get_pricing_by_path(DATA_PATH + '/' + ticker_id + '.csv', '2021-07-01')
    if ticker_data.Volume[-1] < 500000:
        continue
    _1hit_data = ticker_data.tail(10)
    new_data = jModel.convertToJapanCandle(_1hit_data)

    # hasBuySignal = jModel.hasBuySignal(new_data.Open, new_data.Close, new_data.High, new_data.Low,
    #                                    new_data.Body, new_data.Height, new_data.UpShadow,
    #                                    new_data.LowerShadow, new_data.Date)
    hasBuySignal = jModel.hasCustomBuySignal(new_data.Open, new_data.Close, new_data.High, new_data.Low,
                                       new_data.Body, new_data.Height, new_data.UpShadow,
                                       new_data.LowerShadow, 1)

    if hasBuySignal is not False:
        print(ticker_id)

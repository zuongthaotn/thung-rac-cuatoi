import warnings
warnings.filterwarnings('ignore')

import os
import sys
METHOD_MODULE_PATH = os.path.abspath('../..')
sys.path.insert(1, METHOD_MODULE_PATH)
import method.algofuncs as _af
import method.JavCan as jModel

DATA_PATH = os.path.abspath('../../vn-stock-data/VNX/')
# vn30_ticker = _af.getListVN30()
vnx_file = os.path.abspath('../../vn-stock-data/VNX.csv')
hose_ticker = _af.getHOSETickers(vnx_file)

for ticker_id in hose_ticker:
    ticker_data = _af.get_pricing_by_path(DATA_PATH + '/' + ticker_id + '.csv', '2021-07-01')
    _1hit_data = ticker_data.tail(3)
    new_data = jModel.convertToJapanCandle(_1hit_data)
    prices = new_data.Close
    opens = new_data.Open
    bodies = new_data.Body
    ups = new_data.UpShadow
    lows = new_data.LowerShadow
    height = new_data.Height

    isUmbrellaCandlestick = jModel.isUmbrellaCandlestick(bodies[-2], height[-2], ups[-2], lows[-2])
    isWhiteCandlestick = jModel.isWhiteCandlestick(opens[-1], prices[-1])
    if isUmbrellaCandlestick is True and isWhiteCandlestick is True and prices[-1] > prices[-2]:
        print(ticker_id)
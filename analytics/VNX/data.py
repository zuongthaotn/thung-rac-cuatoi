import warnings

warnings.filterwarnings('ignore')

import os
import sys

import method.algofuncs as _af
import method.JavCan as jModel

DATA_PATH = os.path.abspath('vn-stock-data/VNX/')
ticker_id = 'ACB'
ticker_data = _af.get_pricing_by_path(DATA_PATH + '/' + ticker_id + '.csv', '2020-01-01')
# new_data = jModel.convertToJapanCandle(ticker_data)
# print(ticker_data)
def convertToJapanCandle(ticker_data):
    ticker_data['is_green'] = ticker_data.apply(lambda x: 1 if (x['Close'] > x['Open']) else -1, axis=1)

    # ticker_data['Height'] = ticker_data.apply(lambda x: 1 if (x['Close'] > x['Open']) else -1, axis=1)
    ticker_data['Body_on_Height'] = ticker_data.apply(lambda x: (abs(x['Close'] - x['Open']) / abs(x['High'] - x['Low'])) * 100 if (x['High'] > x['Low']) else 0, axis=1)
    # ticker_data['UpShadow'] = ticker_data.apply(
    #     lambda x: (x['High'] - x['Close']) if (x['Close'] > x['Open']) else (x['High'] - x['Open']), axis=1)
    # ticker_data['LowerShadow'] = ticker_data.apply(
    #     lambda x: (x['Open'] - x['Low']) if (x['Close'] > x['Open']) else (x['Close'] - x['Low']), axis=1)
    # if 'Time' in ticker_data.columns:
    #     from datetime import datetime
    #     ticker_data['Date'] = ticker_data.apply(
    #         lambda x: datetime.fromtimestamp(x['Time']).strftime("%m/%d/%Y"), axis=1)
    return ticker_data

new_data = convertToJapanCandle(ticker_data)
print(new_data)
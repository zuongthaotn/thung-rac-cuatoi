import warnings
warnings.filterwarnings('ignore')

import os
import method.algofuncs as _af


DATA_PATH = os.path.abspath('vn-stock-data/VNX/')
ticker_id = 'VCG'
ticker_data = _af.get_pricing_by_path(DATA_PATH + '/' + ticker_id + '.csv', '2013-01-01', '2020-01-06')
print(ticker_data.tail(10))
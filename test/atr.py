import os
import SaleRules as _sr
import algofuncs as _af

DATA_PATH = os.path.abspath('../vn-stock-data/VNX/')
ticker_data = _af.get_pricing_by_path(DATA_PATH + '/' + 'PNJ.csv')
# print(ticker_data)
look_back = 10
look_back_extra = 15
print(_sr.getATR(look_back, ticker_data.High[-look_back_extra:-1], ticker_data.Low[-look_back_extra:-1]))
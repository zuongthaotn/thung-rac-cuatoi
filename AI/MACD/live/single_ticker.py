import pickle
import os
import neat

import warnings
warnings.filterwarnings('ignore')

import sys
import sys_path

sys.path.insert(1, sys_path.BACKTESTING_MODULE_PATH)
import vn_realtime_stock_data.stockHistory as stockHistory
import method.MACD.v1 as v1
import AI.MACD.sources.constants as constants

from datetime import datetime
from datetime import date
from dateutil.relativedelta import relativedelta

def get_signal(macd, signal, ticker):
    config_path = os.path.join(constants.ROOT_DIR, constants.PATH_NEAT_CONF)
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    # load best genome
    best_genome_path = os.path.join(constants.ROOT_DIR, constants.PATH_NEAT_BEST_GENOME, "best_" + ticker)
    best_genome = None
    try:
        with open(best_genome_path, 'rb') as fp:
            best_genome = pickle.load(fp)
    except FileNotFoundError:
        print('You need to train a network first')
        return
    net = neat.nn.FeedForwardNetwork.create(best_genome, config)
    decision = net.activate((macd, signal))
    return decision[0]

ticker = "TSC"

date_from = date.today() + relativedelta(months=-3)
timestamp_from = datetime.strptime(date_from.strftime("%m/%d/%Y") + ', 00:00:0', "%m/%d/%Y, %H:%M:%S").timestamp()
selectedTickers = []
message = '(MACD.AI.v1)Những cổ phiếu đc xem xét: \n'
date_to = date.today()
timestamp_to = datetime.strptime(date_to.strftime("%m/%d/%Y") + ', 23:59:00', "%m/%d/%Y, %H:%M:%S").timestamp()
htd = stockHistory.getStockHistoryData(ticker, timestamp_from, timestamp_to)
prepared_data = v1.prepareData(htd)
yesterday_macd = prepared_data['MACD'][-2]
yesterday_signal = prepared_data['MACDs'][-3]
today_macd = prepared_data['MACD'][-1]
today_signal = prepared_data['MACDs'][-1]
yesterday_stock_market_signal = get_signal(yesterday_macd, yesterday_signal, ticker)
today_stock_market_signal = get_signal(today_macd, today_signal, ticker)
print(yesterday_stock_market_signal)
print(today_stock_market_signal)
if yesterday_stock_market_signal is not None and today_stock_market_signal is not None:
    if yesterday_stock_market_signal < 0.9 and today_stock_market_signal > 0.9:
        selectedTickers.append(ticker)
        message += ticker + "(" + str(prepared_data['Close'][-1]) + ")(MUA)\n"
    # if yesterday_stock_market_signal > 0.1 and today_stock_market_signal < 0.1:
    if today_stock_market_signal < 0.1:
        selectedTickers.append(ticker)
        message += ticker + "(" + str(prepared_data['Close'][-1]) + ")(BÁN)\n"

    if selectedTickers:
        print(message)
    # sendTelegramMessage(message)
print("Done!")

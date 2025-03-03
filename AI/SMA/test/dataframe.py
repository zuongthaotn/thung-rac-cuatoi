
import pickle
import os
import neat
import AI.MACD.sources.constants as constants

import warnings
warnings.filterwarnings('ignore')

import time
import datetime

import sys
import sys_path

sys.path.insert(1, sys_path.BACKTESTING_MODULE_PATH)
from backtesting.backtesting import Backtest, Strategy
import vn_realtime_stock_data.stockHistory as stockHistory
import method.MACD.v1 as v1




def get_signal(macd, signal, macd_h1, macd_h2):
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
    decision = net.activate((macd, signal, macd_h1, macd_h2))
    return decision[0]



def main():
    date_from = "01/01/2022"
    timestamp_from = time.mktime(datetime.datetime.strptime(date_from, "%d/%m/%Y").timetuple())
    date_to = "31/12/2022"
    timestamp_to = time.mktime(datetime.datetime.strptime(date_to, "%d/%m/%Y").timetuple())
    htd = stockHistory.getStockHistoryData(ticker, timestamp_from, timestamp_to)
    prepared_data = v1.prepareData(htd)
    rows_number = len(prepared_data.index)
    get_in = False
    for i in range(20, rows_number):
        macd = prepared_data['MACD'][i]
        signal = prepared_data['MACDs'][i]
        macd_h1 = prepared_data['MACDh'][i-1]
        macd_h2 = prepared_data['MACDh'][i-2]
        date = prepared_data.index[i]
        stock_market_signal = get_signal(macd, signal, macd_h1, macd_h2)
        if stock_market_signal is not None:
            if not get_in and stock_market_signal > 0.5:
                print("Buy --- {} --- with price {}".format(date, prepared_data['Close'][i]))
                get_in = True
            if get_in and stock_market_signal <= 0.5:
                print("Sell --- {} --- with price {}".format(date, prepared_data['Close'][i]))
                get_in = False



if __name__ == '__main__':
    ticker = "MBB"
    main()
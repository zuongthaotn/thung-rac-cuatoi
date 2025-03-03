import pickle
import os
import neat
import AI.SMA.sources.constants as constants

import warnings
warnings.filterwarnings('ignore')

import time
import datetime

import sys
import sys_path

sys.path.insert(1, sys_path.BACKTESTING_MODULE_PATH)
from backtesting.backtesting import Backtest, Strategy
from backtesting.test import SMA
import vn_realtime_stock_data.stockHistory as stockHistory
import method.SMA.v3 as v3


class Sma(Strategy):
    def init(self):
        price = self.data.Close
        self.buy_price = 0
        self.ma5 = self.I(SMA, price, 5)
        self.ma20 = self.I(SMA, price, 20)
        self.sma_r = self.I(lambda: (self.data.SMA_R), name='SMA_R', overlay=False)

    def next(self):
        if (len(self.data.SMA_H) < 23):
            return
        self.current_price = self.data.Close[-1]
        smaR = self.data.SMA_R
        stock_market_signal = get_signal(smaR[-3], smaR[-2], smaR[-1])
        if stock_market_signal is not None:
            if self.buy_price == 0 and stock_market_signal > 0.5:
                self.buy()
                self.buy_price = self.data.Close[-1]
            if self.buy_price != 0 and stock_market_signal <= 0.5:
                self.position.close()
                self.buy_price = 0

def get_signal(smaR_2, smaR_yesterday, smaR_today):
    config_path = os.path.join(constants.ROOT_DIR, constants.PATH_NEAT_CONF)
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    # load best genome
    best_genome_path = os.path.join(constants.ROOT_DIR, constants.PATH_NEAT_BEST_GENOME, "best_" + ticker)
    print(best_genome_path)
    exit()
    best_genome = None
    try:
        with open(best_genome_path, 'rb') as fp:
            best_genome = pickle.load(fp)
    except FileNotFoundError:
        print('You need to train a network first')
        return
    net = neat.nn.FeedForwardNetwork.create(best_genome, config)
    decision = net.activate((smaR_2, smaR_yesterday, smaR_today))
    return decision[0]



def main():
    date_from = "01/01/2022"
    timestamp_from = time.mktime(datetime.datetime.strptime(date_from,"%d/%m/%Y").timetuple())
    date_to = "31/12/2023"
    timestamp_to = time.mktime(datetime.datetime.strptime(date_to,"%d/%m/%Y").timetuple())
    htd = stockHistory.getStockHistoryData(ticker, 1, timestamp_to)
    prepared_data = v3.prepareData(htd)
    bt = Backtest(prepared_data, Sma)
    stats = bt.run()
    print(stats)
    # print(stats['_trades'])
    bt.plot()

if __name__ == '__main__':
    ticker = "MBB"
    main()

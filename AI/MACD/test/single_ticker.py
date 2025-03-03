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


class Macd(Strategy):
    def init(self):
        self.buy_price = 0
        self.macd = self.data.MACD
        self.signal = self.data.MACDs
        self.draw = self.I(lambda: (self.macd, self.signal), name='macd', overlay=False)
        self.draw_h = self.I(lambda: (self.data.MACDh), name='MACDh', overlay=False)

    def next(self):
        self.current_price = self.data.Close[-1]
        macd = self.data.MACD[-1]
        signal = self.data.MACDs[-1]
        signal_h1 = self.data.MACDh[-1]
        signal_h2 = self.data.MACDh[-2]
        stock_market_signal = get_signal(macd, signal, signal_h1, signal_h2)
        if stock_market_signal is not None:
            if self.buy_price == 0 and stock_market_signal > 0.5:
                self.buy()
                self.buy_price = self.data.Close[-1]
            if self.buy_price != 0 and stock_market_signal <= 0.5:
                self.position.close()
                self.buy_price = 0

def get_signal(macd, signal, signal_h1, signal_h2):
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
    decision = net.activate((macd, signal, signal_h1, signal_h2))
    return decision[0]



def main():
    date_from = "01/01/2022"
    timestamp_from = time.mktime(datetime.datetime.strptime(date_from,"%d/%m/%Y").timetuple())
    date_to = "31/12/2023"
    timestamp_to = time.mktime(datetime.datetime.strptime(date_to,"%d/%m/%Y").timetuple())
    htd = stockHistory.getStockHistoryData(ticker, timestamp_from, timestamp_to)
    prepared_data = v1.prepareData(htd)
    bt = Backtest(prepared_data, Macd)
    stats = bt.run()
    print(stats)
    print(stats['_trades'])
    bt.plot()

if __name__ == '__main__':
    ticker = "MBB"
    main()

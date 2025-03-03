import os
import sys
import sys_path
import warnings
warnings.filterwarnings('ignore')

from datetime import datetime
from datetime import date
import time

sys.path.insert(1, sys_path.BACKTESTING_MODULE_PATH)
from backtesting.backtesting import Backtest, Strategy
import vn_realtime_stock_data.stockHistory as stockHistory
import vn_realtime_stock_data.stockRealtimes as stockRealtime
import method.MACD.v1 as v1

import pickle
import neat
import AI.MACD.sources.constants as constants

def get_signal(macd, signal):
    config_path = os.path.join(constants.ROOT_DIR, constants.PATH_NEAT_CONF)
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    # load best genome
    best_genome_path = os.path.join(constants.ROOT_DIR, constants.PATH_NEAT_BEST_GENOME, "best_" + ticker_id)
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

class Macd(Strategy):
    def init(self):
        self.buy_price = 0
        self.macd = self.data.MACD
        self.signal = self.data.MACDs

    def next(self):
        self.current_price = self.data.Close[-1]
        macd = self.data.MACD[-1]
        signal = self.data.MACDs[-1]
        stock_market_signal = get_signal(macd, signal)
        if stock_market_signal is not None:
            if self.buy_price == 0 and stock_market_signal > 0.9:
                self.buy()
                self.buy_price = self.data.Close[-1]
            if self.buy_price != 0 and stock_market_signal < 0.1:
                self.position.close()
                self.buy_price = 0

love_list = stockRealtime.get_vn30_tickers()
love_list.append("REE")
love_list.append("TSC")
love_list.append("VCG")
timestamp_to = datetime.strptime(date.today().strftime("%m/%d/%Y") + ', 23:59:00', "%m/%d/%Y, %H:%M:%S").timestamp()

rows = []
for ticker_id in love_list:
    htd = stockHistory.getStockHistoryData(ticker_id, 1, timestamp_to)
    prepared_data = v1.prepareData(htd)
    bt = Backtest(prepared_data, Macd)
    stats = bt.run()

    if (stats['Sharpe Ratio'] > 0.5):
        rows.append([ticker_id, stats['Return (Ann.) [%]'], stats['Return [%]'], stats['Sharpe Ratio'], stats['Sortino Ratio'], stats['Calmar Ratio']])
    time.sleep(1)

import pandas as pd
df = pd.DataFrame(rows, columns=['Ticker', 'Return (Ann.)', 'Return', 'Sharpe Ratio', 'Sortino Ratio', 'Calmar Ratio'])
import os
local_dir = os.path.dirname(__file__)
new_file = os.path.join(local_dir, 'Ratio_reports.csv')
df.to_csv(new_file, index=False)

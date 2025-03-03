import warnings
warnings.filterwarnings('ignore')

import time
import datetime

import os
import sys
import sys_path

sys.path.insert(1, sys_path.BACKTESTING_MODULE_PATH)
from backtest.backtesting.backtesting import Backtest, Strategy
import vn_realtime_stock_data.stockHistory as stockHistory
import method.EMA.v1 as ema_v1
import AI.EMA.sources.constants as constants
from AI.EMA.sources.broker import Broker
import AI.EMA.sources.signal as signal
import pandas_ta as ta
import pandas as pd

def EMA(arr: pd.Series, n: int) -> pd.Series:
    return ta.ema(pd.Series(arr), length=n)


class Ema(Strategy):
    def init(self):
        price = self.data.Close
        self.buy_price = 0
        self.ema5 = self.I(EMA, price, 5)
        self.ma20 = self.I(EMA, price, 20)
        self.ema_h = self.I(lambda: (self.data.EMA_H), name='EMA_H', overlay=False)
        self.ema_r = self.I(lambda: (self.data.EMA_R), name='EMA_R', overlay=False)
        self.rsi = self.I(lambda: (self.data.RSI_mini), name='RSI_mini', overlay=False)
        self.broker = Broker(constants.STARTING_CAPITAL)

    def next(self):
        if (len(self.data.Close) < 23):
            return
        emaR = self.data.EMA_R
        emaR_2 = emaR[-3]
        emaR_yesterday = emaR[-2]
        emaR_today = emaR[-1]
        rsi = self.data.RSI_mini
        rsi_today = rsi[-1]
        stock_market_signal = signal.get_signal(emaR_2, emaR_yesterday, emaR_today, rsi_today)
        self.broker.do_action(stock_market_signal, self.data.Close[-1])
        if self.buy_price == 0 and self.broker.number_of_stocks > 0:
            self.buy()
            self.buy_price = self.data.Close[-1]
        if self.buy_price != 0 and self.broker.number_of_stocks == 0:
            self.position.close()
            self.buy_price = 0


def run():
    bt = Backtest(prepared_data, Ema)
    stats = bt.run()
    # print(stats)
    with pd.option_context('display.max_rows', None,
                           'display.max_columns', None,
                           'display.precision', 3,
                           ):
        print(stats['_trades'])
    # bt.plot()

if __name__ == '__main__':
    ticker = "DHC"
    # getting data for this generation
    date_from = constants.TEST_FROM_DATE
    timestamp_from = time.mktime(datetime.datetime.strptime(date_from, "%d/%m/%Y").timetuple())
    date_to = constants.TEST_TO_DATE
    timestamp_to = time.mktime(datetime.datetime.strptime(date_to, "%d/%m/%Y").timetuple())
    htd = stockHistory.getStockHistoryData(ticker, timestamp_from, timestamp_to)
    prepared_data = ema_v1.prepareData(htd)
    config_path = os.path.join(constants.ROOT_DIR, constants.PATH_NEAT_CONF)
    best_genome_path = os.path.join(constants.ROOT_DIR, constants.PATH_NEAT_BEST_GENOME,
                                    ticker + constants.GENOME_BRAIN_POSTFIX)
    print("Testing from {} to {}".format(date_from, date_to))
    print("Getting best genome/brain from file: \n {}".format(best_genome_path))
    signal.set_ticker(ticker)
    run()

import pandas as pd
import neat
import os
import pickle

from datetime import datetime
from datetime import date
from dateutil.relativedelta import relativedelta

import sys
import sys_path
import AI.MACD.sources.constants as constants
from AI.MACD.sources.bookmaker import Bookmaker
sys.path.insert(1, sys_path.BACKTESTING_MODULE_PATH)
import vn_realtime_stock_data.stockHistory as stockHistory
import vn_realtime_stock_data.stockRealtimes as stockRealtime
import method.MACD.v1 as v1
from multiprocessing import Pool

def training(genomes, config):
    global prepared_data
    # We have x number of genomes. X is specified in the configuration file
    # for ever genome we will create one object of Bookmaker class, this object will simulate behaviour of the person
    # which buys and sells stocks
    # Also for each genome we create a neural network
    bookmakers = []
    nets = []
    ge = []
    # Creating individual data for every object in this generation
    for _, genome in genomes:
        bookmaker = Bookmaker(constants.STARTING_CAPITAL)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        genome.fitness = 0
        bookmakers.append(bookmaker)
        nets.append(net)
        ge.append(genome)

    data_set = prepared_data[constants.CSV_OPEN_COLUMN]
    macd = prepared_data['MACD']
    signal = prepared_data['MACDs']
    rows_number = len(prepared_data.index)

    # starting simulation, from 20 because we need to omit all the zeroes that appears during calculating MACD
    for i in range(20, rows_number):
        for j in range(0, len(bookmakers)):
            try:
                decision = nets[j].activate((macd[i], signal[i]))  # decision can be a real number form 0 to 1
            except (IndexError, ValueError):
                continue

            # if there is a missing data cell, then substitute it with the latest stock value
            index = i
            while pd.isnull(data_set[index]):
                index -= 1
            if decision[0] > 0.9:
                if bookmakers[j].canBuyMore(data_set[index]):
                    bookmakers[j].buy_all_stocks(data_set[index])
            elif decision[0] < 0.1:
                if bookmakers[j].canSellStock():
                    bookmakers[j].sell_all_stocks(data_set[index])

                    # Increase fitness when bookmaker sold stock with profit
                    # Decrease fitness when bookmaker sold stock with loss
                    difference = bookmakers[j].incomes - bookmakers[j].expenses
                    ge[j].fitness += difference

                    # bookmaker is bankrupt, so delete it from further trading
                    if bookmakers[j].capital < bookmakers[j].equity_peak * 0.65:
                        ge[j].fitness = 0
                        nets.pop(bookmakers.index(bookmakers[j]))
                        ge.pop(bookmakers.index(bookmakers[j]))
                        bookmakers.pop(bookmakers.index(bookmakers[j]))




def run(ticker):
    print("Ticker: ", ticker)
    global prepared_data
    config_path = os.path.join(constants.ROOT_DIR, constants.PATH_NEAT_CONF)
    # creating configuration basing on our configuration file
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)


    # getting data for this generation
    timestamp_to = datetime.strptime(date.today().strftime("%m/%d/%Y") + ', 23:59:00',
                                     "%m/%d/%Y, %H:%M:%S").timestamp()
    htd = stockHistory.getStockHistoryData(ticker, 1, timestamp_to)
    prepared_data = v1.prepareData(htd)
    # creating population basing on our configuration
    population = neat.Population(config)

    # creating reporter that will print crucial data in the terminal
    # population.add_reporter(neat.StdOutReporter(True))
    # stats = neat.StatisticsReporter()
    # population.add_reporter(stats)

    # saving the best genome after completing the training
    winner = population.run(training, constants.NUMBER_OF_GENERATIONS)

    # statistics of the best genome
    print('\nBest genome:\n{!s}'.format(winner))

    # save the best genome to a file
    save_path = os.path.join(constants.ROOT_DIR, constants.PATH_NEAT_BEST_GENOME, "best_" + ticker)
    with open(save_path, 'wb') as fp:
        pickle.dump(winner, fp)

if __name__ == '__main__':
    prepared_data = None
    vn30 = stockRealtime.get_vn30_tickers()
    # ignores = []
    # tickers = []
    # for given_ticker in vn30:
    #     if given_ticker in ignores:
    #         continue
    #     tickers.append(given_ticker)
    #
    with Pool(10) as pool:
        # perform calculations
        results = pool.map(run, vn30)
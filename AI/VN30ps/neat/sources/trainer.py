import neat
import os
import pickle
import numpy as np
import pandas_ta as ta
import pandas as pd
import time
from datetime import datetime

import vn_realtime_stock_data.stockHistory as stockHistory
import AI.VN30ps.neat.sources.constants as constants

prepared_data = emaR = rsi = []
ticker = ''
rows_number = 0


def prepare_data():
    global prepared_data, emaR, rsi, rows_number
    # getting data for this generation
    date_to = "31/10/2022"
    timestamp_to = time.mktime(datetime.strptime(date_to, "%d/%m/%Y").timetuple())
    htd = stockHistory.getStockHistoryData(ticker, 1, timestamp_to)
    if 'Time' in htd.columns:
        htd['DateStr'] = htd.apply(
            lambda x: datetime.fromtimestamp(x['Time']).strftime("%Y-%m-%d"), axis=1)

    htd['Today_Green'] = htd.apply(
        lambda x: True if x['Close'] >= x['Open'] else False, axis=1)

    htd["EMA_5"] = ta.ema(htd["Close"], length=5)
    htd["EMA_20"] = ta.ema(htd["Close"], length=20)
    htd['EMA_H'] = htd.apply(
        lambda x: (x['EMA_20'] - x['EMA_5']), axis=1)
    htd['EMA_R'] = htd.apply(
        lambda x: ((x['EMA_5'] - x['EMA_20']) * 10 / x['EMA_5']), axis=1)
    htd["RSI_20"] = ta.rsi(htd["Close"], length=20, fillna=True)
    htd['RSI_mini'] = htd.apply(
        lambda x: (x['RSI_20'] / 100), axis=1)
    htd['Date'] = pd.to_datetime(htd['DateStr'])
    ticker_data = htd.set_index('Date')
    prepared_data = ticker_data.drop(columns=['Time', 'DateStr', 'High', 'Low', 'Volume'])
    prepared_data['EMA_5'] = ticker_data['EMA_5'].replace(np.nan, 0)
    prepared_data['EMA_20'] = ticker_data['EMA_20'].replace(np.nan, 0)
    prepared_data['EMA_H'] = ticker_data['EMA_H'].replace(np.nan, 0)
    prepared_data['EMA_H'] = ticker_data['EMA_H'].round(0)
    prepared_data['EMA_R'] = ticker_data['EMA_R'].replace(np.nan, 0)
    prepared_data['Tomorrow_Green'] = ticker_data.Today_Green.shift(-1)
    emaR = prepared_data['EMA_R']
    rsi = prepared_data['RSI_mini']
    rows_number = len(prepared_data.index)


def set_ticker(new_value):
    global ticker
    ticker = new_value


def ema_train(genomes, config):
    global prepared_data
    if not len(prepared_data):
        print("No prepared data.")
        exit()

    nets = []
    ge = []
    # Creating individual data for every object in this generation
    for _, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        genome.fitness = 0
        nets.append(net)
        ge.append(genome)

    for i in range(23, rows_number):
        is_tomorrow_green = prepared_data['Tomorrow_Green'][i]
        for j in range(0, len(ge)):
            # decision can be a real number form 0 to 1
            decision = nets[j].activate((emaR[i - 2], emaR[i - 1], emaR[i], rsi[i]))
            if decision[0] <= 0.5:      # has sell signal
                if not is_tomorrow_green:
                    ge[j].fitness += 5
                if is_tomorrow_green:
                    ge[j].fitness -= 10

            if decision[0] > 0.5:      # has buy signal
                if is_tomorrow_green:
                    ge[j].fitness += 5
                if not is_tomorrow_green:
                    ge[j].fitness -= 10

def run(on_ticker):
    set_ticker(on_ticker)
    if not ticker:
        print("No ticker selected.")
        exit()
    print("Ticker: ", ticker)
    prepare_data()
    config_path = os.path.join(constants.ROOT_DIR, constants.PATH_NEAT_CONF)
    best_genome_path = os.path.join(constants.ROOT_DIR, constants.PATH_NEAT_BEST_GENOME,
                                    ticker + constants.GENOME_BRAIN_POSTFIX)
    # creating configuration basing on our configuration file
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    if config.genome_config.activation_default != constants.ACTIVATION_FUNCS:
        print("Check the activation functions again, they are unsync.")
        exit()
    # creating population basing on our configuration
    population = neat.Population(config)

    # creating reporter that will print crucial data in the terminal
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    """
        saving the best genome after completing the training
    """
    winner = population.run(ema_train, constants.NUMBER_OF_GENERATIONS)
    # winner = population.run(training, 1)

    """
        statistics of the best genome
    """
    print('\nBest genome:\n{!s}'.format(winner))
    print("Saving best genome/brain to file: \n {}" . format(best_genome_path))
    # save the best genome to a file
    with open(best_genome_path, 'wb') as fp:
        pickle.dump(winner, fp)

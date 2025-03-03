import time

import neat
import os
import pickle
from datetime import datetime
from datetime import date

import vn_realtime_stock_data.stockHistory as stockHistory
import method.EMA.v1 as ema_v1
import AI.EMA.sources.constants as constants
from AI.EMA.sources.broker import Broker

prepared_data = emaR = rsi = []
ticker = ''
rows_number = 0


def prepare_data():
    global prepared_data, emaR, rsi, rows_number
    # getting data for this generation
    timestamp_to = datetime.strptime(date.today().strftime("%m/%d/%Y") + ', 00:00:00', "%m/%d/%Y, %H:%M:%S").timestamp()
    htd = stockHistory.getStockHistoryData(ticker, 1, timestamp_to)
    prepared_data = ema_v1.prepareData(htd)
    emaR = prepared_data['EMA_R']
    rsi = prepared_data['RSI_mini']
    rows_number = len(prepared_data.index)
    # print("Data length: {}" . format(rows_number))


def set_ticker(new_value):
    global ticker
    ticker = new_value


def ema_train(genomes, config):
    global prepared_data
    if not len(prepared_data):
        print("No prepared data.")
        exit()
    # We have x number of genomes. X is specified in the configuration file
    # forever genome we will create one object of Broker class, this object will simulate behaviour of the person
    # which buys and sells stocks
    # Also for each genome we create a neural network
    brokers = []
    nets = []
    ge = []
    # Creating individual data for every object in this generation
    for _, genome in genomes:
        broker = Broker(constants.STARTING_CAPITAL)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        genome.fitness = 0
        brokers.append(broker)
        nets.append(net)
        ge.append(genome)

    # starting simulation, from 20 because we need to omit all the zeroes that appears during calculating MACD
    alive_brokers = brokers
    alive_ge = ge
    alive_nets = nets
    for i in range(23, rows_number):
        today_price = prepared_data['Close'][i]
        brokers = alive_brokers
        alive_brokers = []
        ge = alive_ge
        alive_ge = []
        nets = alive_nets
        alive_nets = []
        # today_date = prepared_data.index[i]
        for j in range(0, len(brokers)):
            # decision can be a real number form 0 to 1
            decision = nets[j].activate((emaR[i - 2], emaR[i - 1], emaR[i], rsi[i]))
            # brokers[j].do_action(decision, today_price, today_date)
            brokers[j].do_action(decision, today_price)
            if brokers[j].profit:
                ge[j].fitness += brokers[j].profit
                if brokers[j].profit > 0:
                    ge[j].fitness += 5
                else:
                    ge[j].fitness -= 10
            if not brokers[j].is_alive:
                ge[j].fitness -= 100000
            else:
                alive_brokers.append(brokers[j])
                alive_ge.append(ge[j])
                alive_nets.append(nets[j])

    if len(alive_brokers) > 0:
        for k in range(0, len(alive_brokers)):
            if not alive_brokers[k].num_transaction:
                ge[k].fitness = 0
            else:
                ge[k].fitness = ge[k].fitness * alive_brokers[k].win_trades / alive_brokers[k].num_transaction

    #     print("Alive broker: {}".format(len(brokers)))
    #     time.sleep(2)
    # print("------------------------------------")
    # print(len(alive_brokers))
    # show_reports(alive_brokers, alive_ge)

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
    # population.add_reporter(neat.StdOutReporter(True))
    # stats = neat.StatisticsReporter()
    # population.add_reporter(stats)

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

def show_reports(alive_brokers, alive_ge):
    if len(alive_brokers) > 0:
        the_best_broker = 0
        the_worst_broker = 0
        capital_peak = 0
        capital_valley = alive_brokers[0].capital
        for k in range(0, len(alive_brokers)):
            if alive_brokers[k].number_of_stocks:
                alive_brokers[k].sell_all_stocks(prepared_data['Close'][-1])
            if alive_brokers[k].capital > capital_peak:
                capital_peak = alive_brokers[k].capital
                the_best_broker = k
            if alive_brokers[k].capital < capital_valley:
                capital_valley = alive_brokers[k].capital
                the_worst_broker = k

        the_best_gen = 0
        the_worst_gen = 0
        fitness_peak = 0
        fitness_valley = alive_ge[0].fitness
        for f in range(0, len(alive_ge)):
            if alive_ge[f].fitness > fitness_peak:
                fitness_peak = alive_ge[f].fitness
                the_best_gen = f
            if alive_ge[f].fitness < fitness_valley:
                fitness_valley = alive_ge[f].fitness
                the_worst_gen = f

        print("------------------------------------------")
        print("Alive broker(s): {}".format(len(alive_brokers)))
        print("The best broker ID: {}".format(the_best_broker))
        print("Capital: {}".format(alive_brokers[the_best_broker].capital))
        print("The best fitness: {}".format(fitness_peak))
        print("The best genome ID: {}".format(the_best_gen))
        print("Total transactions: {}".format(alive_brokers[the_best_broker].num_transaction))
        print("-----------")
        print("The worst broker ID: {}".format(the_worst_broker))
        print("Capital: {}".format(alive_brokers[the_worst_broker].capital))
        print("The worst fitness: {}".format(fitness_valley))
        print("The worst genome ID: {}".format(the_worst_gen))
        print("Total transactions: {}".format(alive_brokers[the_worst_broker].num_transaction))
        # exit()
        # print("Total Transactions:")
        # for tran in alive_brokers[the_best_broker].history:
        #     print(tran)